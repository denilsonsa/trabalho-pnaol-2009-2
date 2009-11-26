import bpy
import Blender
import random
import sys

Blender.Window.EditMode(0)

bola_material = None
iteration = []
bola = []

def new_ball(raio, name="Bola"):
    # Creating the mesh
    mesh = Blender.Mesh.Primitives.UVsphere(16,16,2*raio)
    if name:
        mesh.name = name+"Mesh"

    # Setting smooth rendering
    for f in mesh.faces:
        f.smooth = True

    # Adding vertex colors
    color_red   = random.randrange(0,256)
    color_green = random.randrange(0,256)
    color_blue  = random.randrange(0,256)
    mesh.vertexColors = True
    for f in mesh.faces:
        for i,v in enumerate(f):
            f.col[i].r = color_red
            f.col[i].g = color_green
            f.col[i].b = color_blue

    # Setting the default Material for this ball
    mesh.materials = [bola_material]
    # Too bad the following lines don't work...
    #mesh.setMaterials([bola_material])
    #obj.setMaterials([bola_material])

    # Creating the actual object that contains the mesh
    scn = bpy.data.scenes.active
    obj = scn.objects.new(mesh, name)

    # Adding a subsurf modifier (just to make it even prettier)
    subsurf = obj.modifiers.append(Blender.Modifier.Types.SUBSURF)

    subsurf[Blender.Modifier.Settings.RENDER] = 1
    subsurf[Blender.Modifier.Settings.REALTIME] = 0
    subsurf[Blender.Modifier.Settings.EDITMODE] = 0

    subsurf[Blender.Modifier.Settings.LEVELS] = 1
    subsurf[Blender.Modifier.Settings.RENDLEVELS] = 1

    return obj


def new_ball_material():
    mat = Blender.Material.New('BolaMat')
    mat.setMode(mat.getMode() | Blender.Material.Modes.VCOL_PAINT)
    #mat.setMode(* 'SHADOW SHADOWBUF TRACEABLE RAYBIAS TANGENTSTR RADIO VCOL_PAINT'.split())
    return mat


def array(points):
    "Função usada dentro do execfile() ao ler o arquivo 'points.txt'."
    global iteration
    iteration.append(points)

def main():
    global bola_material, iteration

    bola_material = new_ball_material()

    execfile("points.txt", globals())

    scaling = 100.0

    for i in range(numbolas):
        bola.append( new_ball(
            raio[i]/scaling,
            name = "Bola%3d" % (i+1,)
        ))

    it = iteration[0]
    for i,coords in enumerate(it[1:]):
        bola[i].setLocation(
            coords[0]/scaling,
            coords[1]/scaling,
            coords[2]/scaling
        )

    Blender.Redraw()


if __name__ == "__main__":
    main()


def unused_code():
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

