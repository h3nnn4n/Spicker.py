import pyrosetta
import sys


pyrosetta.init()

basename = sys.argv[1]
names = sys.argv[2:]

total_pose = 0
pose_names = []

plen = 0

out = basename + '.tra1'

scorefxn = pyrosetta.get_fa_scorefxn()

def get_psize():
    size = 0
    name = names[0]
    pose = pyrosetta.pose_from_pdb(name)

    for i in range(pose.total_residue()):
        for j in range(pose.residue(i + 1).natoms()):
            if pose.residue(i + 1).atom(j + 1).type() == 24:
                size += 1
                break

    return size

psize = get_psize()

with open(out, 'wt') as f:
    for name in names:
        pose = pyrosetta.pose_from_pdb(name)
        plen = pose.total_residue()
        pose_names.append(out)
        score = scorefxn(pose)

        f.write("%8d %10.3f %6d %6d\n" % (
            psize, score, total_pose + 1, total_pose + 1)
        )

        for i in range(pose.total_residue()):
            for j in range(pose.residue(i + 1).natoms()):
                if pose.residue(i + 1).atom(j + 1).type() == 24:
                    coords = pose.residue(i + 1).atom(j + 1).xyz()
                    f.write(" %9.3f %9.3f %9.3f\n" % (coords.x, coords.y, coords.z))
                    break

        total_pose += 1

with open('tra.in', 'wt') as f:
    f.write("%d %d %d\n" % (1, -1, 1))
    f.write("%s\n" % out)

with open('rmsinp', 'wt') as f:
    f.write("%d %d\n" % (1, psize))
    f.write("%d\n" % (psize))

pose = pyrosetta.pose_from_pdb(names[0])

with open('seq.dat', 'wt') as f:
    for n in range(pose.total_residue()):
        f.write("%4d %3s\n" % (n + 1, pose.residue(n + 1).name3()))
