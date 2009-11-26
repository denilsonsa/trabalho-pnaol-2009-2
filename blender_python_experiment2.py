import bpy
import Blender
import random
import sys

Blender.Window.EditMode(0)

bola_material = None
iterations = []
bolas = []

def new_ball(raio, name="Bola"):
    mesh = new_ball_mesh(raio, name)

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

    # Creating an empty IPO curve
    ipo = Blender.Ipo.New("Object", name+"Ipo")

    for curvename in ("LocX", "LocY", "LocZ"):
        ipocurve = ipo.addCurve(curvename)
        ipocurve.extend = Blender.IpoCurve.ExtendTypes["CONST"]
        ipocurve.interpolation = Blender.IpoCurve.InterpTypes["BEZIER"]

    obj.setIpo(ipo)

    return obj


def new_ball_material():
    mat = Blender.Material.New('BolaMat')
    mat.setMode(mat.getMode() | Blender.Material.Modes.VCOL_PAINT)
    #mat.setMode(* 'SHADOW SHADOWBUF TRACEABLE RAYBIAS TANGENTSTR RADIO VCOL_PAINT'.split())
    return mat


def new_ball_mesh(raio, name="Bola"):
    # Creating the mesh
    mesh = Blender.Mesh.Primitives.UVsphere(16, 16, 2*raio)
    mesh.name = name + "Mesh"

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

    return mesh


def new_bezier_point(x, y, knot_len=1):
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


def array(points):
    "Função usada dentro do execfile() ao ler o arquivo 'points.txt'."
    global iterations
    iterations.append(points)


def main():
    global bola_material, iterations

    bola_material = new_ball_material()

    scaling = 100.0

    execfile("points.txt", globals())

    # Creating and adding balls to the global "bolas" list
    for i in range(numbolas):
        bolas.append( new_ball(
            raio[i]/scaling,
            name = "Bola%03d" % (i+1,)
        ))

    frames_per_iteration = 25

    # Moving the balls using IPO curves
    for i in range(numbolas):
        obj = bolas[i]
        curvex = obj.getIpo()[Blender.Ipo.OB_LOCX]
        curvey = obj.getIpo()[Blender.Ipo.OB_LOCY]
        curvez = obj.getIpo()[Blender.Ipo.OB_LOCZ]

        # Adding the coordinates
        for itnum, it in enumerate(iterations):
            coord = it[i+1]
            curvex.append(new_bezier_point(1 + itnum*frames_per_iteration, coord[0]/scaling))
            curvey.append(new_bezier_point(1 + itnum*frames_per_iteration, coord[1]/scaling))
            curvez.append(new_bezier_point(1 + itnum*frames_per_iteration, coord[2]/scaling))

        #curvex.recalc()
        #curvey.recalc()
        #curvez.recalc()

    Blender.Redraw()


if __name__ == "__main__":
    main()
