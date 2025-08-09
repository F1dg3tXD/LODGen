# LODGen — Generate LODs for Games in 3 Clicks or Less

**LODGen** is a Blender 4.4 addon designed to simplify Level of Detail (LOD) creation for game assets.  
Quickly generate multiple LOD meshes with progressive decimation — all within Blender’s 3D View, no complex setup required.

---

## Generate LODs for Games in 3 Clicks or Less
### ***Yes, I counted :skull:***

Select your meshes, add them to the list, and hit generate. That’s it.

---

## Features

- Add multiple objects to the LOD generation list with one click  
- Control decimation scale per LOD step via a simple slider  
- Set number of LOD iterations (default: 6)  
- Original meshes are preserved and hidden, preventing data loss  
- Generates LOD0 as a clean base with modifiers applied  
- Automatically creates and reuses dedicated LOD collections per object  
- Progressive decimation applied cumulatively for realistic LOD levels  
- Seamless workflow integration in the 3D View **N-panel** under the **Create** tab  

---

## Installation

1. Download from here, or get it on the Blender Extensions Platform.  
   - [Pending Approval](https://extensions.blender.org/approval-queue/lod-gen)  

2. Enable the addon in Blender via **Edit → Preferences → Add-ons → LODGen**  

---

## Usage

1. Select the mesh objects you want to create LODs for.  
2. Click **Add Selected Objects** in the LODGen panel (3D View → Sidebar → Create → LODGen).  
3. Adjust **Decimation Scale** and **Iterations** as desired (default 0.5 scale, 6 iterations).  
4. Hit **Generate LODs** and watch the magic happen.  

Your original meshes remain untouched (just hidden), and LODs appear neatly organized in dedicated collections.

---

## License

This addon is licensed under the **GNU General Public License v3.0 (GPL-3.0)**

See [LICENSE](./LICENSE) for details.

---

## Contributing

Contributions, suggestions, and bug reports are welcome!  
Feel free to open issues or pull requests on the repo.

---

## Support & Contact

If you find this addon useful or have questions, reach out via the repo or contact me via Discord. [F1dg3t's Workshop](https://discord.gg/HE6YhEcFfz).
