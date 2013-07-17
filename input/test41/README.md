Test 41
=====================
Disc source of neutron onto vacuum cylinder. There are 8 scoring volumes in
the problem. Each Volume is seperated from the last by incling the split surface
by 10 degrees previous to the last. So the angle of the surface seperating
V1 and V2 is 10 degree, from V2 to V3 is 20 degrees, until the end where V7 and
V8 are seperated by 80 degree surface.

              +-----------------------------------+   
  ----->     /         \                         / \
  ----->    /           \                       /   \
  ----->   |             \                     |     | 
  ----->    \             \                     \   /
  ----->     \             \                     \ /
              +-----------------------------------+
            10.0                                182.0

Again, normalising the area of each surface to be 1.0, we expect the flux 
crossing each surface to be given by 1/cos(theta). We expect excellent agreement
in this benchmark.
           
Quantities Tested
=====================
* Proton Irradiation
* Medium energy irradiation
* USRTRACK scoring
* Transport in Vacuum