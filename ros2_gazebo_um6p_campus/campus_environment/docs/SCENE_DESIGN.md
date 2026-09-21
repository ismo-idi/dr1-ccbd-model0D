# Scene design and future staging space

This is a photograph-inspired architectural approximation. Dimensions are in metres, angles in radians unless explicitly marked degrees. No survey, structural engineering validation, official logo, flight capacity or mathematical safety certificate is implied.

| Feature | Final assumption |
|---|---|
| Courtyard | 64 x 60, centered at (0,5), paved top z=0 |
| Pergola | 28 x 18 footprint; x[-14,14], y[0,18] |
| Roof curve | z(x)=8.6+1.35*cos(pi*x/28), segmented at 1m |
| Lattice | main repeated members at about 2m intervals |
| Branching supports | six, bases at x=-10,0,10 and y=3,15 |
| Rear building translation | +12m Y from first approved visual draft |
| Clear gap | canopy rear edge y=18 to foremost facade band y=31.8: 13.8m |
| Landmark | origin(-7,0,0), four 1.6m blocks with narrow gaps on plinth |
| Landmark rotations, top down | U:+12deg, M:-12deg, 6:+12deg, P:-12deg |
| Letter faces | local front(-Y) and right(+X), rotated with each block |
| Current UAV/pad centers | (-3.6,-8.2) and (3.6,-8.2); 7.2m center spacing |
| UAV model-origin height | z=.12 on .12m pads; skids roughly .005m above pad |
| Empty forecourt reserve | x[-9,9], y[-22,-4]: 18 x 18 = 324m² |

The staging reserve is unmarked so the approved paving and landscaping stay unchanged. It is clear of the pergola, landmark, buildings, planters, benches and palms; only the two movable-in-a-future-revision display pads/vehicles occupy it. It establishes an area to consider in separately authorized expansion. It does not certify that 3, 5, 10, 20 or 100 flying vehicles can safely fit, nor does it prescribe formation spacing. Capacity depends on future vehicle size, dynamics, clearances, flight height, boundaries and protocol. If 100 vehicles require more area, expansion must be separately scoped; there is no active automatic spawn/count parameter now.

UAVs are first-party static visual placeholders. They have no animated joints or propellers, flight-ready inertial/aerodynamic data or controllers. Decorative campus meshes are not validated physical collision bodies. The small UAV body collision box is only a placeholder.

Following the user's requested adjustments, the pergola, architecture shapes, palms, planting beds, benches, paving pattern, colors, lighting and UAV shapes remained unchanged. Only tower block/letter rotations, building world pose, pad positions and UAV world poses changed; camera framing was adjusted for inspection. `evidence/feedback-change-scope.json` records the byte-level description mesh comparison.
