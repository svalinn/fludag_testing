Test 1
=====================
Neutron irradiation on vacuum geometry, parallel plane beam of neutrons 

      	      +----+----+-~~-+----+----+
Neutrons     / V2 / V3 /    / V8 / V9 /|
            +----+----+-~~-+----+----+ |
-->         |    |    |    |    |    | +
            |    |    |    |    |    |/
            +----+----+-~~-+----+----+ 

Track length flux estimate in every volume, every volume has the volume used to normalise
the particle score to 1.0, in this example we expect particles starting beyond V2 
travelling through to V9 to contribute the same track length to each score. Due to the exact
faceting of the CAD model in this instance, we expect exact agreement between Fluka and FluDAG

Quantities Tested
=====================
* Neutron Irradiation
* Vacuum transport
* Low energy irradiation
* USRTRACK scoring