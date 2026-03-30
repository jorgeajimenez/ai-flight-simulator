const fs = require('fs');
let code = fs.readFileSync('index.html', 'utf-8');

// 1. Fix the Texture Fetch (Pre-rasterize SVG to Canvas)
const oldFetch = `                let sharedBuildingMaterial;
                try {
                    const textureRes = await fetch(\`/texture?prompt=\${theme}\`);
                    const textureData = await textureRes.json();
                    sharedBuildingMaterial = new Cesium.ImageMaterialProperty({
                        image: "data:image/svg+xml;base64," + textureData.image,
                        repeat: new Cesium.Cartesian2(1, 1),
                    });
                } catch (e) {`;

const newFetch = `                let sharedBuildingMaterial;
                try {
                    const textureRes = await fetch(\`/texture?prompt=\${theme}\`);
                    const textureData = await textureRes.json();
                    
                    // PERFORMANCE FIX: Pre-rasterize SVG to a Canvas. 
                    // Cesium will freeze rendering hundreds of entities with raw SVG Data URIs.
                    const img = new Image();
                    img.src = "data:image/svg+xml;base64," + textureData.image;
                    await new Promise(r => { img.onload = r; img.onerror = r; });
                    const canvas = document.createElement("canvas");
                    canvas.width = 1024;
                    canvas.height = 1024;
                    const ctx = canvas.getContext("2d");
                    ctx.drawImage(img, 0, 0, 1024, 1024);

                    sharedBuildingMaterial = new Cesium.ImageMaterialProperty({
                        image: canvas,
                        repeat: new Cesium.Cartesian2(2, 6), // Tile vertically for skyscrapers
                    });
                } catch (e) {`;

code = code.replace(oldFetch, newFetch);

// 2. Remove terrible looking Orbs and Arches to clean up the skyline
const oldShapes = `                        if (shapeType < 0.15) {`;
const newShapes = `                        if (false) { // Disabled Orbs/Arches for better aesthetics`;

code = code.replace(oldShapes, newShapes);

fs.writeFileSync('index.html', code);
console.log("index.html patched.");
