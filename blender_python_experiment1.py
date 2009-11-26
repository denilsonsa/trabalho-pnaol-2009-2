# http://wiki.blender.org/index.php/Doc:Manual/Extensions/Python
# http://wiki.blender.org/index.php/Doc:Manual/Extensions/Python/Example
#
# http://blenderartists.org/forum/showthread.php?t=3736


import bpy
import Blender

Blender.Window.EditMode(0)

s = Blender.Mesh.Primitives.UVsphere(16,16,2)
for f in s.faces:
    f.smooth = True

# http://www.blender.org/documentation/248PythonDoc/Object-module.html#New
scn = bpy.data.scenes.active
obj = scn.objects.new(s, "Sphere")
obj.setLocation(2,2,2)
obj.setSize(1,2,0.5)

# http://www.blender.org/documentation/249PythonDoc/Modifier-module.html
subsurf = obj.modifiers.append(Blender.Modifier.Types.SUBSURF)

subsurf[Blender.Modifier.Settings.RENDER] = 1
subsurf[Blender.Modifier.Settings.REALTIME] = 0
subsurf[Blender.Modifier.Settings.EDITMODE] = 0

subsurf[Blender.Modifier.Settings.LEVELS] = 1
subsurf[Blender.Modifier.Settings.RENDLEVELS] = 1


ipo = Blender.Ipo.New("Object", "GeneratedIpo")
ipocurve = ipo.addCurve("dLocZ")
ipocurve.extend = Blender.IpoCurve.ExtendTypes["CONST"]
ipocurve.interpolation = Blender.IpoCurve.InterpTypes["BEZIER"]

knot_len = 1
def newBezier(x,y):
    # Note: the knot_len is completely ignored when handleTypes are set to AUTO,
    # i.e., Blender will calculate new positions for the handles automatically.
    b = Blender.BezTriple.New( (
        x-knot_len, y, 0,
        x, y, 0,
        x+knot_len, y, 0,
    ) )
    # Bezier handle types:
    # http://wiki.blender.org/index.php/Doc:Manual/Modelling/Curves#B.C3.A9ziers
    b.handleTypes = [
        Blender.BezTriple.HandleTypes["AUTO"],
        Blender.BezTriple.HandleTypes["AUTO"],
    ]
    return b

b1 = newBezier(0,10)
b2 = newBezier(200,0)

# AttributeError: attribute 'bezierPoints' of 'IpoCurve' objects is not writable
# ipocurve.bezierPoints += [b1,b2]

ipocurve.append(b1)
ipocurve.append(b2)

obj.setIpo(ipo)
Blender.Redraw()


# Using PyDrivers could be very nice!
# http://wiki.blender.org/index.php/Dev:Source/Blender/2.42/PyDrivers
# http://wiki.blender.org/index.php/Doc:Manual/Animation/Advanced/Driven_Shape_Keys/PyDrivers
