"""Builds the course's Grasshopper definitions (.gh) from code, so they can be rebuilt.

Runs inside Rhino (8 or 9), not with uv. Through the Rhino MCP server's run_python:

    import runpy
    runpy.run_path(r"<repo>/scripts/make_gh.py")["main"]()

or open it in Rhino's ScriptEditor and run it. Writes into kits/, next to each tool's contract.
Only GH1 components that Rhino 8 also has.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Canvas:
    """A small helper for placing and wiring objects on a new GH1 document."""

    def __init__(self):
        import Rhino
        Rhino.RhinoApp.GetPlugInObject("Grasshopper")
        import Grasshopper
        import System
        self.gh, self.System = Grasshopper, System
        self.doc = Grasshopper.Kernel.GH_Document()

    def _place(self, obj, x, y, nick=None):
        if nick:
            obj.NickName = nick
        obj.CreateAttributes()
        obj.Attributes.Pivot = self.System.Drawing.PointF(x, y)
        self.doc.AddObject(obj, False)
        return obj

    def component(self, name, x, y, where=None):
        """Place a component by name. `where` ("Maths" or "Maths > Operators") picks between components
        that share a name (Addition, Rotate...)."""
        for proxy in self.gh.Instances.ComponentServer.ObjectProxies:
            d = proxy.Desc
            if d.Name != name or proxy.Obsolete or (where and f"{d.Category} > {d.SubCategory}".find(where) != 0):
                continue
            obj = proxy.CreateInstance()
            if hasattr(obj, "Params"):
                return self._place(obj, x, y)
        raise KeyError(f"No Grasshopper component called {name}" + (f" in {where}" if where else ""))

    def constant(self, param, *values):
        """Give an input fixed value(s), replacing any default it came with."""
        param.PersistentData.Clear()
        for v in values:
            if param.Type.IsInterface:  # takes any kind of value (Maths operators, Ladybug's inputs)
                goo = self.gh.Kernel.GH_Convert.ToGoo(v)
            else:  # takes its own value type only
                goo = self.System.Activator.CreateInstance(param.Type)
                if not goo.CastFrom(v):
                    raise ValueError(f"{param.Name} can't take {v!r}")
            param.PersistentData.Append(goo)

    def output(self, nick, source, x, y, panel=False):
        """A named output: a Panel (shows its value on the canvas) or a plain parameter."""
        if panel:
            out = self.panel(nick, x, y)
        else:
            out = self._place(self.gh.Kernel.Parameters.Param_Geometry(), x, y, nick)
        out.AddSource(source)
        return out

    def slider(self, nick, low, value, high, x, y, decimals=0):
        s = self.gh.Kernel.Special.GH_NumberSlider()
        acc = self.gh.GUI.Base.GH_SliderAccuracy
        s.Slider.Type = acc.Float if decimals else acc.Integer
        s.Slider.DecimalPlaces = decimals
        s.Slider.Minimum, s.Slider.Maximum = self.System.Decimal(low), self.System.Decimal(high)
        s.SetSliderValue(self.System.Decimal(value))
        return self._place(s, x, y, nick)

    def panel(self, nick, x, y):
        p = self.gh.Kernel.Special.GH_Panel()
        p.UserText = ""
        return self._place(p, x, y, nick)

    def choice(self, nick, items, x, y, selected=0):
        """A Value List (a dropdown): [(name, text value), ...]. The runner only accepts these names."""
        special = self.gh.Kernel.Special
        v = special.GH_ValueList()
        v.ListItems.Clear()
        for name, value in items:
            v.ListItems.Add(special.GH_ValueListItem(name, f'"{value}"'))
        v.ListMode = special.GH_ValueListMode.DropDown
        v.SelectItem(selected)
        return self._place(v, x, y, nick)

    def geometry(self, nick, x, y):
        return self._place(self.gh.Kernel.Parameters.Param_Geometry(), x, y, nick)

    def note(self, text, x, y, size=20):
        s = self.gh.Kernel.Special.GH_Scribble()
        s.Text = text
        s.Font = self.System.Drawing.Font("Arial", size)
        return self._place(s, x, y)

    def group(self, name, objects, rgb):
        g = self.gh.Kernel.Special.GH_Group()
        g.NickName = name
        g.Colour = self.System.Drawing.Color.FromArgb(120, *rgb)
        for o in objects:
            g.AddObject(o.InstanceGuid)
        return self._place(g, 0, 0)

    def wire(self, source, target):
        target.AddSource(source)

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not self.gh.Kernel.GH_DocumentIO(self.doc).SaveQuiet(str(path)):
            raise IOError(f"Could not save {path}")
        print("wrote", path.relative_to(ROOT).as_posix())


INPUTS, OUTPUTS = (120, 200, 255), (255, 210, 120)  # blue-ish and orange-ish groups


def make_sum():
    """sum: two numbers in, their sum out. The Grasshopper version of Session 1's add tool."""
    c = Canvas()
    c.note("sum: adds two numbers", 40, 20)
    a = c.slider("in:a", 0, 1, 1000, 40, 100, decimals=2)
    b = c.slider("in:b", 0, 2, 1000, 40, 150, decimals=2)
    add = c.component("Addition", 330, 125)
    c.wire(a, add.Params.Input[0])
    c.wire(b, add.Params.Input[1])
    out = c.panel("out:sum", 470, 110)
    c.wire(add.Params.Output[0], out)
    c.group("Inputs", [a, b], INPUTS)
    c.group("Outputs", [out], OUTPUTS)
    c.save(ROOT / "kits" / "gh" / "tools" / "sum" / "sum.gh")


def make_tower():
    """tower: Session 1's tower, rebuilt in Grasshopper. Must match build() in kits/tower/tools/tower/tower.py.

    For each floor, t runs from 0 (ground) to 1 (top). A width x depth rectangle centred on the
    origin is scaled by 1 + (taper - 1) t, rotated by twist t, and moved by lean t towards
    lean_dir and up by floor number x floor height. Each outline is extruded one floor up.
    """
    c = Canvas()
    M, V, T = "Maths > Operators", "Vector > Vector", "Transform > Euclidean"
    c.note("tower: the Session 1 tower, in Grasshopper", 40, 0, 24)
    sl = {}
    for i, (nick, low, value, high, decimals) in enumerate([
            ("floors", 1, 12, 80, 0), ("floor_height", 2.8, 3.5, 6.0, 2), ("width", 6, 20, 60, 1),
            ("depth", 6, 20, 60, 1), ("twist", -360, 0, 360, 0), ("taper", 0.2, 1.0, 2.0, 2),
            ("lean", 0, 0, 40, 1), ("lean_dir", 0, 0, 360, 0)]):
        sl[nick] = c.slider("in:" + nick, low, value, high, 40, 80 + 50 * i, decimals)
    inputs_group = list(sl.values())  # the plot joins this group below

    # t for each floor: a range from 0 to 1 in (floors - 1) steps; z: a series 0, h, 2h...
    x = 380
    steps = c.component("Subtraction", x, 80, M)
    c.wire(sl["floors"], steps.Params.Input[0]); c.constant(steps.Params.Input[1], 1)
    t = c.component("Range", x + 140, 80)
    c.wire(steps.Params.Output[0], t.Params.Input[1])
    t_out = t.Params.Output[0]
    z = c.component("Series", x + 140, 160)
    c.constant(z.Params.Input[0], 0)
    c.wire(sl["floor_height"], z.Params.Input[1]); c.wire(sl["floors"], z.Params.Input[2])
    c.group("1 · Each floor: t from 0 (ground) to 1 (top), and its height z", [steps, t, z], (200, 200, 200))

    # scale = 1 + (taper - 1) t ; angle = twist t ; lean offset = lean t, towards lean_dir
    y = 280
    tm1 = c.component("Subtraction", x, y, M)
    c.wire(sl["taper"], tm1.Params.Input[0]); c.constant(tm1.Params.Input[1], 1)
    tt = c.component("Multiplication", x + 140, y, M)
    c.wire(tm1.Params.Output[0], tt.Params.Input[0]); c.wire(t_out, tt.Params.Input[1])
    scale = c.component("Addition", x + 280, y, M)
    c.constant(scale.Params.Input[0], 1); c.wire(tt.Params.Output[0], scale.Params.Input[1])
    tw = c.component("Multiplication", x, y + 80, M)
    c.wire(sl["twist"], tw.Params.Input[0]); c.wire(t_out, tw.Params.Input[1])
    angle = c.component("Radians", x + 140, y + 80)
    c.wire(tw.Params.Output[0], angle.Params.Input[0])
    ln = c.component("Multiplication", x, y + 160, M)
    c.wire(sl["lean"], ln.Params.Input[0]); c.wire(t_out, ln.Params.Input[1])
    heading = c.component("Radians", x, y + 240)
    c.wire(sl["lean_dir"], heading.Params.Input[0])
    sin, cos = c.component("Sine", x + 140, y + 220), c.component("Cosine", x + 140, y + 270)
    c.wire(heading.Params.Output[0], sin.Params.Input[0]); c.wire(heading.Params.Output[0], cos.Params.Input[0])
    dx, dy = c.component("Multiplication", x + 280, y + 180, M), c.component("Multiplication", x + 280, y + 250, M)
    for d, trig in ((dx, sin), (dy, cos)):
        c.wire(ln.Params.Output[0], d.Params.Input[0]); c.wire(trig.Params.Output[0], d.Params.Input[1])
    move_by = c.component("Vector XYZ", x + 420, y + 200, V)
    c.wire(dx.Params.Output[0], move_by.Params.Input[0]); c.wire(dy.Params.Output[0], move_by.Params.Input[1])
    c.wire(z.Params.Output[0], move_by.Params.Input[2])
    c.group("2 · How much each floor is scaled, turned and shifted", [tm1, tt, scale, tw, angle, ln, heading, sin, cos,
                                                                    dx, dy, move_by], (200, 200, 200))

    # the ground-floor rectangle, centred on the origin, then scale, rotate, move
    x2, y2 = 960, 80
    parts = []
    domains = []
    for i, key in enumerate(("width", "depth")):
        half = c.component("Division", x2, y2 + 90 * i, M)
        c.wire(sl[key], half.Params.Input[0]); c.constant(half.Params.Input[1], 2)
        neg = c.component("Negative", x2 + 120, y2 + 90 * i + 20, M)
        c.wire(half.Params.Output[0], neg.Params.Input[0])
        dom = c.component("Construct Domain", x2 + 240, y2 + 90 * i)
        c.wire(neg.Params.Output[0], dom.Params.Input[0]); c.wire(half.Params.Output[0], dom.Params.Input[1])
        parts += [half, neg, dom]
        domains.append(dom)
    rect = c.component("Rectangle", x2 + 380, y2 + 40, "Curve")
    c.wire(domains[0].Params.Output[0], rect.Params.Input[1]); c.wire(domains[1].Params.Output[0], rect.Params.Input[2])
    scaled = c.component("Scale", x2 + 520, y2 + 140, "Transform")
    c.wire(rect.Params.Output[0], scaled.Params.Input[0]); c.wire(scale.Params.Output[0], scaled.Params.Input[2])
    turned = c.component("Rotate", x2 + 660, y2 + 140, T)
    c.wire(scaled.Params.Output[0], turned.Params.Input[0]); c.wire(angle.Params.Output[0], turned.Params.Input[1])
    placed = c.component("Move", x2 + 800, y2 + 140, T)
    c.wire(turned.Params.Output[0], placed.Params.Input[0]); c.wire(move_by.Params.Output[0], placed.Params.Input[1])
    up = c.component("Unit Z", x2 + 660, y2 + 300, V)
    c.wire(sl["floor_height"], up.Params.Input[0])
    solid = c.component("Extrude", x2 + 800, y2 + 300, "Surface")
    c.wire(placed.Params.Output[0], solid.Params.Input[0]); c.wire(up.Params.Output[0], solid.Params.Input[1])
    capped = c.component("Cap Holes", x2 + 940, y2 + 300, "Surface")
    c.wire(solid.Params.Output[0], capped.Params.Input[0])
    area = c.component("Area", x2 + 940, y2 + 420, "Surface")
    c.wire(placed.Params.Output[0], area.Params.Input[0])
    gfa = c.component("Mass Addition", x2 + 1080, y2 + 420, M)
    c.wire(area.Params.Output[0], gfa.Params.Input[0])
    height = c.component("Multiplication", x2 + 1080, y2 + 520, M)
    c.wire(sl["floors"], height.Params.Input[0]); c.wire(sl["floor_height"], height.Params.Input[1])
    c.group("3 · Each floor's outline, and a block one floor high", parts + [rect, scaled, turned, placed, up, solid,
                                                                       capped, area, gfa, height], (200, 200, 200))

    # beyond the plot: for every floor corner outside the plot, its distance to the plot's edge; the largest
    import Rhino
    g = Rhino.Geometry
    plot = c._place(c.gh.Kernel.Parameters.Param_Curve(), 40, 520, "in:plot")
    c.constant(plot, g.Rectangle3d(g.Plane.WorldXY, g.Point3d(-15, -15, 0), g.Point3d(15, 15, 0)).ToNurbsCurve())
    x3, y3 = 960, 700
    corners = c.component("Control Points", x3, y3, "Curve")
    c.wire(placed.Params.Output[0], corners.Params.Input[0])
    flat3d = c.component("Flatten Tree", x3 + 60, y3, "Sets > Tree")
    c.wire(corners.Params.Output[0], flat3d.Params.Input[0])
    xyz = c.component("Deconstruct", x3 + 120, y3 + 120, "Vector > Point")
    c.wire(flat3d.Params.Output[0], xyz.Params.Input[0])
    flat = c.component("Construct Point", x3 + 180, y3 + 120, "Vector > Point")  # the corner dropped to the ground
    c.wire(xyz.Params.Output[0], flat.Params.Input[0]); c.wire(xyz.Params.Output[1], flat.Params.Input[1])
    inside = c.component("Point In Curve", x3 + 240, y3 - 40, "Curve")
    c.wire(flat.Params.Output[0], inside.Params.Input[0]); c.wire(plot, inside.Params.Input[1])
    outside = c.component("Smaller Than", x3 + 380, y3 - 40, "Maths")  # Point In Curve: 0 outside, 1 on, 2 inside
    c.wire(inside.Params.Output[0], outside.Params.Input[0]); c.constant(outside.Params.Input[1], 1)
    edge = c.component("Curve Closest Point", x3 + 240, y3 + 60, "Curve")
    c.wire(flat.Params.Output[0], edge.Params.Input[0]); c.wire(plot, edge.Params.Input[1])
    keep = c.component("Dispatch", x3 + 520, y3, "Sets > List")
    c.wire(edge.Params.Output[2], keep.Params.Input[0]); c.wire(outside.Params.Output[0], keep.Params.Input[1])
    none = c.component("Merge", x3 + 640, y3, "Sets > Tree")  # add a 0, so a tower inside the plot gives 0
    c.wire(keep.Params.Output[0], none.Params.Input[0]); c.constant(none.Params.Input[1], 0.0)
    order = c.component("Sort List", x3 + 760, y3, "Sets > List")
    c.wire(none.Params.Output[0], order.Params.Input[0])
    furthest = c.component("List Item", x3 + 880, y3, "Sets > List")
    c.wire(order.Params.Output[0], furthest.Params.Input[0]); c.constant(furthest.Params.Input[1], -1)
    c.group("4 · How far any floor corner reaches beyond the plot (0 if the tower stays inside)",
            [corners, flat3d, xyz, flat, inside, outside, edge, keep, none, order, furthest], (200, 200, 200))
    c.group("Inputs: the eight tower parameters, and the plot", inputs_group + [plot], INPUTS)

    outs = [c.output("out:floors", placed.Params.Output[0], x2 + 1260, y2 + 140),
            c.output("out:mass", capped.Params.Output[0], x2 + 1260, y2 + 300),
            c.output("out:gfa_m2", gfa.Params.Output[0], x2 + 1260, y2 + 420, panel=True),
            c.output("out:height_m", height.Params.Output[0], x2 + 1260, y2 + 520, panel=True),
            c.output("out:beyond_plot_m", furthest.Params.Output[0], x2 + 1260, y2 + 620, panel=True)]
    c.group("Outputs", outs, OUTPUTS)
    c.save(ROOT / "kits" / "site" / "tools" / "tower" / "tower.gh")


# Cities for sun measures: name; latitude; longitude; time zone (standard time, hours from UTC).
# Ladybug can't look a city up by name, so the list is on the canvas. Add a city by adding a line.
CITIES = [
    ("London", 51.51, -0.13, 0), ("Paris", 48.86, 2.35, 1), ("Berlin", 52.52, 13.40, 1),
    ("Copenhagen", 55.68, 12.57, 1), ("Rotterdam", 51.92, 4.48, 1), ("Vienna", 48.21, 16.37, 1),
    ("Milan", 45.46, 9.19, 1), ("Barcelona", 41.39, 2.17, 1), ("Bucharest", 44.43, 26.10, 2),
    ("Athens", 37.98, 23.73, 2), ("New York", 40.71, -74.01, -5), ("Singapore", 1.35, 103.82, 8),
    ("Sydney", -33.87, 151.21, 10),
]


def make_sun_lost(tool, target, context, note):
    """A sun measure: hours of direct sun on `target` on 21 March, and how much of it the tower takes away.

    Runs Ladybug twice: with the tower (and any context) casting shadows, and without the tower (an empty
    plot). The UK's BRE guide (BR 209) treats keeping less than 0.8 times the former sunlight (a loss of
    more than 20%) as a noticeable loss.
    """
    c = Canvas()
    LB = "Ladybug"
    c.note(note, 40, 0, 24)
    tower = c.geometry("in:tower", 40, 80)
    others = [c.geometry("in:context", 40, 130)] if context else []
    park = c.geometry("in:" + target, 40, 180)
    city = c.choice("in:city", [(n, f"{n};{lat};{lon};{tz}") for n, lat, lon, tz in CITIES], 40, 240)
    c.group("Inputs", [tower, *others, park, city], INPUTS)

    split = c.component("Text Split", 260, 240)
    c.wire(city, split.Params.Input[0]); c.constant(split.Params.Input[1], ";")
    parts = []
    for i in range(4):
        item = c.component("List Item", 400, 200 + 60 * i, "Sets > List")
        c.wire(split.Params.Output[0], item.Params.Input[0]); c.constant(item.Params.Input[1], i)
        parts.append(item)
    where = c.component("LB Construct Location", 560, 240, LB)
    for item, nick in zip(parts, ("_name_", "_latitude_", "_longitude_", "_time_zone_")):
        c.wire(item.Params.Output[0], next(p for p in where.Params.Input if p.NickName == nick))
    day = c.component("LB Analysis Period", 560, 400, LB)
    for nick, value in (("_start_month_", 3), ("_start_day_", 21), ("_end_month_", 3), ("_end_day_", 21), ("_timestep_", 4)):
        c.constant(next(p for p in day.Params.Input if p.NickName == nick), value)
    sun = c.component("LB SunPath", 760, 300, LB)
    c.wire(where.Params.Output[0], next(p for p in sun.Params.Input if p.NickName == "_location"))
    c.wire(next(p for p in day.Params.Output if p.NickName == "hoys"), next(p for p in sun.Params.Input if p.NickName == "hoys_"))
    c.group("1 · Where and when: the sun's positions every 15 minutes on 21 March", [split, *parts, where, day, sun],
            (200, 200, 200))

    def sun_hours(y, casting, title):
        """Direct sun hours at points 2 m apart on the target, with `casting` throwing shadows; and their average."""
        hours = c.component("LB Direct Sun Hours", 960, y, LB)
        inp = {p.NickName: p for p in hours.Params.Input}
        c.wire(next(p for p in sun.Params.Output if p.NickName == "vectors"), inp["_vectors"])
        c.constant(inp["_timestep_"], 4)
        c.wire(park, inp["_geometry"])
        for source in casting:
            c.wire(source, inp["context_"])
        c.constant(inp["_grid_size"], 2.0)
        c.constant(inp["_run"], True)
        mean = c.component("Average", 1160, y + 40)
        c.wire(next(p for p in hours.Params.Output if p.NickName == "results"), mean.Params.Input[0])
        c.group(title, [hours, mean], (200, 200, 200))
        return hours, mean

    with_tower, mean = sun_hours(80, [tower, *others], f"2 · Sun on the {target} with the tower")
    _, empty = sun_hours(380, others, f"3 · Sun on the {target} with an empty plot")
    lost = c.component("Subtraction", 1320, 260, "Maths > Operators")
    c.wire(empty.Params.Output[0], lost.Params.Input[0]); c.wire(mean.Params.Output[0], lost.Params.Input[1])
    ratio = c.component("Division", 1460, 260, "Maths > Operators")
    c.wire(lost.Params.Output[0], ratio.Params.Input[0]); c.wire(empty.Params.Output[0], ratio.Params.Input[1])
    percent = c.component("Multiplication", 1600, 260, "Maths > Operators")
    c.wire(ratio.Params.Output[0], percent.Params.Input[0]); c.constant(percent.Params.Input[1], 100)
    c.group("4 · Sun lost = (empty plot − with tower) ÷ empty plot", [lost, ratio, percent], (200, 200, 200))

    mesh = next(p for p in with_tower.Params.Output if p.NickName == "mesh")
    outs = [c.output("out:sun_hours", mean.Params.Output[0], 1800, 60, panel=True),
            c.output("out:sun_hours_empty_plot", empty.Params.Output[0], 1800, 150, panel=True),
            c.output("out:sun_lost_percent", percent.Params.Output[0], 1800, 240, panel=True),
            c.output("out:sun_map", mesh, 1800, 340),
            c.output("out:location", where.Params.Output[0], 1800, 400, panel=True)]
    c.group("Outputs", outs, OUTPUTS)
    c.save(ROOT / "kits" / "measures" / "tools" / tool / f"{tool}.gh")


def make_park_sun():
    make_sun_lost("park_sun", "park", True, "park_sun: sun on the park on 21 March (Ladybug)")


def make_river_view():
    """river_view: how much of the tower people on the river see (Ladybug's Visibility Percent).

    Each point 2 m apart on the tower's surface gets the share of viewpoints that can see it, with the
    neighbours (and the tower itself) in the way. Seen area = that share, averaged, x the surface area.
    """
    c = Canvas()
    LB = "Ladybug"
    c.note("river_view: how much of the tower people on the river see (Ladybug)", 40, 0, 24)
    tower, context, views = c.geometry("in:tower", 40, 80), c.geometry("in:context", 40, 130), c.geometry("in:viewpoints", 40, 180)
    c.group("Inputs", [tower, context, views], INPUTS)
    seen = c.component("LB Visibility Percent", 300, 80, LB)
    inp = {p.NickName: p for p in seen.Params.Input}
    c.wire(views, inp["_view_points"]); c.wire(tower, inp["_geometry"]); c.wire(context, inp["context_"])
    c.constant(inp["_grid_size"], 2.0)
    c.constant(inp["_run"], True)
    out = {p.NickName: p for p in seen.Params.Output}
    share = c.component("Average", 520, 60)
    c.wire(out["results"], share.Params.Input[0])
    surface = c.component("Area", 520, 160, "Surface")
    c.wire(out["mesh"], surface.Params.Input[0])
    product = c.component("Multiplication", 660, 100, "Maths > Operators")
    c.wire(share.Params.Output[0], product.Params.Input[0]); c.wire(surface.Params.Output[0], product.Params.Input[1])
    area = c.component("Division", 800, 100, "Maths > Operators")
    c.wire(product.Params.Output[0], area.Params.Input[0]); c.constant(area.Params.Input[1], 100)
    c.group("1 · For each point on the tower: the % of viewpoints that see it. Seen area = average % × surface",
            [seen, share, surface, product, area], (200, 200, 200))
    outs = [c.output("out:seen_m2", area.Params.Output[0], 980, 60, panel=True),
            c.output("out:view_map", out["mesh"], 980, 160)]
    c.group("Outputs", outs, OUTPUTS)
    c.save(ROOT / "kits" / "measures" / "tools" / "river_view" / "river_view.gh")


def make_terraces():
    """terraces: the open roof each floor leaves where the floor above steps back or turns.

    Floor outlines sorted bottom to top; for each floor, its outline minus the one above it (Region
    Difference, on that floor's plane). Built-in components only.
    """
    c = Canvas()
    L, M = "Sets > List", "Maths > Operators"
    c.note("terraces: open roof left where the floor above steps back", 40, 0, 24)
    floors = c.geometry("in:floors", 40, 80)
    c.group("Inputs", [floors], INPUTS)
    area = c.component("Area", 200, 80, "Surface")
    c.wire(floors, area.Params.Input[0])
    xyz = c.component("Deconstruct", 330, 100, "Vector > Point")
    c.wire(area.Params.Output[1], xyz.Params.Input[0])
    order = c.component("Sort List", 460, 80, L)
    c.wire(xyz.Params.Output[2], order.Params.Input[0]); c.wire(floors, order.Params.Input[1])
    below, below_z = c.component("Cull Index", 600, 40, "Sets > Sequence"), c.component("Cull Index", 600, 160, "Sets > Sequence")
    for cull, source in ((below, order.Params.Output[1]), (below_z, order.Params.Output[0])):
        c.wire(source, cull.Params.Input[0]); c.constant(cull.Params.Input[1], -1); c.constant(cull.Params.Input[2], True)
    above = c.component("Shift List", 600, 100, L)
    c.wire(order.Params.Output[1], above.Params.Input[0]); c.constant(above.Params.Input[1], 1); c.constant(above.Params.Input[2], False)
    origin = c.component("Construct Point", 740, 160, "Vector > Point")
    c.wire(below_z.Params.Output[0], origin.Params.Input[2])
    plane = c.component("XY Plane", 860, 160, "Vector > Plane")
    c.wire(origin.Params.Output[0], plane.Params.Input[0])
    c.group("1 · Floors from bottom to top: each floor (except the top) with the floor above it",
            [area, xyz, order, below, below_z, above, origin, plane], (200, 200, 200))
    grafted = []
    for i, source in enumerate((below.Params.Output[0], above.Params.Output[0], plane.Params.Output[0])):
        g = c.component("Graft Tree", 1000, 40 + 60 * i, "Sets > Tree")
        c.wire(source, g.Params.Input[0])
        grafted.append(g)
    terrace = c.component("Region Difference", 1140, 80, "Intersect")
    for g, inp in zip(grafted, terrace.Params.Input):
        c.wire(g.Params.Output[0], inp)
    shapes = c.component("Boundary Surfaces", 1280, 40, "Surface")
    c.wire(terrace.Params.Output[0], shapes.Params.Input[0])
    each = c.component("Area", 1400, 40, "Surface")  # of the surfaces: a ring-shaped terrace keeps its hole
    c.wire(shapes.Params.Output[0], each.Params.Input[0])
    flat = c.component("Flatten Tree", 1520, 40, "Sets > Tree")
    c.wire(each.Params.Output[0], flat.Params.Input[0])
    none = c.component("Merge", 1640, 80, "Sets > Tree")  # add a 0, so a tower with no terraces gives 0
    c.wire(flat.Params.Output[0], none.Params.Input[0]); c.constant(none.Params.Input[1], 0.0)
    total = c.component("Mass Addition", 1760, 40, M)
    c.wire(none.Params.Output[0], total.Params.Input[0])
    sizes = c.component("Sort List", 1760, 140, L)
    c.wire(none.Params.Output[0], sizes.Params.Input[0])
    largest = c.component("List Item", 1880, 140, L)
    c.wire(sizes.Params.Output[0], largest.Params.Input[0]); c.constant(largest.Params.Input[1], -1)
    c.group("2 · Terrace = a floor minus the floor above it. Add them up, and find the largest",
            [*grafted, terrace, shapes, each, flat, none, total, sizes, largest], (200, 200, 200))
    outs = [c.output("out:terrace_m2", total.Params.Output[0], 2040, 60, panel=True),
            c.output("out:largest_terrace_m2", largest.Params.Output[0], 2040, 150, panel=True),
            c.output("out:terraces", shapes.Params.Output[0], 2040, 240)]
    c.group("Outputs", outs, OUTPUTS)
    c.save(ROOT / "kits" / "measures" / "tools" / "terraces" / "terraces.gh")


def make_neighbours_sun():
    """The neighbours are measured and also block their own sun, so they need no separate context."""
    make_sun_lost("neighbours_sun", "neighbours", False, "neighbours_sun: sun on the neighbouring buildings on 21 March (Ladybug)")


# The site: Session 1's wish, "a 30 x 30 m plot next to a park, noticed from the river". Metres, north = +y.
SITE = {
    "Plot": {"rectangle": (-15, -15, 15, 15)},
    "Park": {"surface": (-45, 27, 45, 87)},  # across a 12 m street, north of the plot: the tower's shadow falls on it
    "River": {"surface": (-160, 110, 160, 150)},
    "River views": {"points": [(x, 130, 1.6) for x in range(-120, 121, 40)]},  # eye height, mid-river
    "Neighbours": {"boxes": [(-45, -15, -21, 15, 18), (21, -15, 45, 15, 24), (-45, -55, 45, -27, 15),
                             (-95, 27, -57, 87, 21), (57, 27, 95, 87, 18)]},
}
SITE_COLOURS = {"Plot": (200, 40, 40), "Park": (90, 160, 80), "River": (70, 130, 200), "River views": (30, 80, 160),
                "Neighbours": (150, 150, 150)}


def make_site():
    """site.3dm: plot, park, river, viewpoints on the river and neighbouring blocks, saved for Rhino 8 and 9."""
    import Rhino
    import System
    g = Rhino.Geometry
    model = Rhino.FileIO.File3dm()
    model.Settings.ModelUnitSystem = Rhino.UnitSystem.Meters
    model.Settings.ModelAbsoluteTolerance = 0.001
    parent = Rhino.DocObjects.Layer()
    parent.Name = "Site"
    model.AllLayers.Add(parent)
    parent_id = model.AllLayers.FindName("Site", System.Guid.Empty).Id
    for name, things in SITE.items():
        layer = Rhino.DocObjects.Layer()
        layer.Name, layer.ParentLayerId = name, parent_id
        layer.Color = System.Drawing.Color.FromArgb(*SITE_COLOURS[name])
        model.AllLayers.Add(layer)
        index = model.AllLayers.FindName(name, parent_id).Index
        attributes = Rhino.DocObjects.ObjectAttributes()
        attributes.LayerIndex = index
        for kind, value in things.items():
            if kind == "rectangle":
                x0, y0, x1, y1 = value
                model.Objects.AddCurve(g.Rectangle3d(g.Plane.WorldXY, g.Point3d(x0, y0, 0), g.Point3d(x1, y1, 0))
                                       .ToNurbsCurve(), attributes)
            elif kind == "surface":
                x0, y0, x1, y1 = value
                surface = g.PlaneSurface(g.Plane.WorldXY, g.Interval(x0, x1), g.Interval(y0, y1))
                model.Objects.AddBrep(g.Brep.CreateFromSurface(surface), attributes)
            elif kind == "points":
                for p in value:
                    model.Objects.AddPoint(g.Point3d(*p), attributes)
            elif kind == "boxes":
                for x0, y0, x1, y1, h in value:
                    box = g.Box(g.Plane.WorldXY, g.Interval(x0, x1), g.Interval(y0, y1), g.Interval(0, h))
                    model.Objects.AddBrep(box.ToBrep(), attributes)
    path = ROOT / "kits" / "site" / "site" / "site.3dm"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not model.Write(str(path), 8):
        raise IOError(f"Could not write {path}")
    print("wrote", path.relative_to(ROOT).as_posix())


def main():
    make_sum()
    make_tower()
    make_site()
    make_park_sun()
    make_neighbours_sun()
    make_river_view()
    make_terraces()


if __name__ == "__main__":
    main()
