import pyrosetta
import sys
import os


pyrosetta.init()

names = sys.argv[1:]

total_pose = 0
pose_names = []

plen = 0

for name in names:
    pose = pyrosetta.pose_from_pdb(name)
    plen = pose.total_residue()
    out = os.path.splitext(os.path.basename(name))[0] + '.tra1'
    pose_names.append(out)
    with open(out, 'wt') as f:
        f.write("%d 0.0 1 1\n" % pose.total_residue())
        for i in range(pose.total_residue()):
            for j in range(pose.residue(i + 1).natoms()):
                if pose.residue(i + 1).atom(j + 1).type() == 24:
                    coords = pose.residue(i + 1).atom(j + 1).xyz()
                    f.write("%10.5f %10.5f %10.5f\n" % (coords[1], coords[2], coords[3]))
                    break

    total_pose += 1

with open('tra.in', 'wt') as f:
    f.write("%d\n" % total_pose)
    for name in pose_names:
        f.write("%s\n" % name)

with open('rmsinp', 'wt') as f:
    f.write("%d %d\n" % (1, plen))
    f.write("%d\n" % (plen))
