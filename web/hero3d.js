/* MixMind hero — real-time 3D paver scene (three.js, self-hosted vendor build).
   Recreates the approved v8 render live: charcoal pavers (top-only chamfer glb),
   key/fill/amber-rim lighting, rising CO2 particles that die at the amber
   "cement cut" plane. Pointer-drag rotates the scene. */
import * as THREE from "three";
import { GLTFLoader } from "./vendor/GLTFLoader.js";

export function mountHero3D(container, onReady) {
  const W = () => container.clientWidth, H = () => container.clientHeight;

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(W(), H());
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  Object.assign(renderer.domElement.style, {
    position: "absolute", inset: "0", width: "100%", height: "100%",
    borderRadius: "14px", cursor: "grab", touchAction: "pan-y" });
  container.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(34, W() / H(), 0.1, 60);
  camera.position.set(2.35, 0.85, 3.05);
  camera.lookAt(0, 0.22, 0);

  /* ---- procedural charcoal-concrete texture (crisp at any size, no compression) ---- */
  function concreteTexture(sizePx, speckN, base) {
    const c = document.createElement("canvas"); c.width = c.height = sizePx;
    const g = c.getContext("2d");
    g.fillStyle = base; g.fillRect(0, 0, sizePx, sizePx);
    const img = g.getImageData(0, 0, sizePx, sizePx), d = img.data;
    for (let i = 0; i < d.length; i += 4) {          // per-pixel grain
      const n = (Math.random() - 0.5) * 14;
      d[i] += n; d[i + 1] += n; d[i + 2] += n;
    }
    g.putImageData(img, 0, 0);
    for (let i = 0; i < speckN; i++) {               // aggregate specks
      const a = 0.22 + Math.random() * 0.5, r = Math.random() * 1.6 + 0.4;
      g.fillStyle = `rgba(${175 + Math.random() * 50},${170 + Math.random() * 45},${160 + Math.random() * 40},${a})`;
      g.beginPath();
      g.arc(Math.random() * sizePx, Math.random() * sizePx, r, 0, 7);
      g.fill();
    }
    const t = new THREE.CanvasTexture(c);
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.colorSpace = THREE.SRGBColorSpace;
    return t;
  }
  const mat = new THREE.MeshStandardMaterial({
    map: concreteTexture(1024, 1500, "#3b3e45"),
    roughness: 0.92, metalness: 0.0,
  });

  /* ---- ground ---- */
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(40, 40),
    new THREE.MeshStandardMaterial({ color: 0x1c1e23, roughness: 0.96 }));
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);

  /* ---- pavers (approved v8 geometry) ---- */
  const group = new THREE.Group();
  scene.add(group);
  new GLTFLoader().load("assets/paver.glb", (glb) => {
    let mesh = null;
    glb.scene.traverse((o) => { if (o.isMesh && !mesh) mesh = o; });
    const geo = mesh.geometry;
    geo.center();
    geo.computeVertexNormals();
    const bb = new THREE.Box3().setFromBufferAttribute(geo.attributes.position);
    const halfH = (bb.max.y - bb.min.y) / 2;

    function paver(x, z, rotY) {
      const m = new THREE.Mesh(geo, mat);
      m.position.set(x, halfH + 0.001, z);
      m.rotation.y = rotY;
      m.castShadow = m.receiveShadow = true;
      group.add(m);
      return m;
    }
    paver(0.30, 0.30, THREE.MathUtils.degToRad(-24));   // hero
    paver(-1.05, -0.85, THREE.MathUtils.degToRad(38));  // companion
    if (onReady) onReady();
  });

  /* ---- lights: key / fill / amber rim (v8 recipe) ---- */
  const key = new THREE.DirectionalLight(0xffffff, 2.6);
  key.position.set(2.4, 3.4, 2.2);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.camera.left = key.shadow.camera.bottom = -4;
  key.shadow.camera.right = key.shadow.camera.top = 4;
  key.shadow.radius = 6;
  scene.add(key);
  scene.add(new THREE.HemisphereLight(0x3a3f4a, 0x101114, 0.9));
  const rim = new THREE.SpotLight(0xffb757, 16, 12, Math.PI / 7, 0.75, 1.8);
  rim.position.set(-1.0, 1.6, -3.4);
  rim.target.position.set(0.3, 0.25, 0.3);
  scene.add(rim, rim.target);

  /* ---- CO2 particles: rise from the hero paver, die at the amber cut plane ---- */
  const CUT_Y = 1.00, N = 80;
  const pGeo = new THREE.BufferGeometry();
  const pos = new Float32Array(N * 3), age = new Float32Array(N), life = new Float32Array(N);
  function respawn(i) {
    pos[i * 3] = 0.30 + (Math.random() - 0.5) * 0.5;
    pos[i * 3 + 1] = 0.62 + Math.random() * 0.25;
    pos[i * 3 + 2] = 0.30 + (Math.random() - 0.5) * 0.3;
    age[i] = 0; life[i] = 5 + Math.random() * 4;
  }
  for (let i = 0; i < N; i++) { respawn(i); age[i] = Math.random() * life[i]; }
  pGeo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  const sprite = (() => {                          // soft round smoke sprite
    const c = document.createElement("canvas"); c.width = c.height = 64;
    const g = c.getContext("2d");
    const rg = g.createRadialGradient(32, 32, 2, 32, 32, 30);
    rg.addColorStop(0, "rgba(190,192,198,0.55)");
    rg.addColorStop(1, "rgba(190,192,198,0)");
    g.fillStyle = rg; g.fillRect(0, 0, 64, 64);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  })();
  const pMat = new THREE.PointsMaterial({
    size: 0.26, map: sprite, transparent: true, opacity: 0.22,
    depthWrite: false, blending: THREE.NormalBlending });
  const points = new THREE.Points(pGeo, pMat);
  group.add(points);

  /* ---- interaction: drag to rotate, gentle idle sway ---- */
  let targetRot = 0, rot = 0, dragging = false, lastX = 0, idle = 0;
  const el = renderer.domElement;
  el.addEventListener("pointerdown", (e) => { dragging = true; lastX = e.clientX; el.style.cursor = "grabbing"; });
  window.addEventListener("pointerup", () => { dragging = false; el.style.cursor = "grab"; });
  window.addEventListener("pointermove", (e) => {
    if (!dragging) return;
    targetRot += (e.clientX - lastX) * 0.005;
    targetRot = Math.max(-0.9, Math.min(0.9, targetRot));
    lastX = e.clientX; idle = -4;                   // pause sway after user input
  });

  /* ---- loop ---- */
  const clock = new THREE.Clock();
  let raf = 0;
  function tick() {
    const dt = Math.min(clock.getDelta(), 0.05);
    idle += dt;
    if (!dragging && idle > 0) targetRot += Math.sin(clock.elapsedTime * 0.25) * 0.0004;
    rot += (targetRot - rot) * 0.06;
    group.rotation.y = rot;

    for (let i = 0; i < N; i++) {                   // smoke life-cycle
      age[i] += dt;
      if (age[i] > life[i]) respawn(i);
      const t = age[i] / life[i];
      pos[i * 3 + 1] += dt * (0.11 + t * 0.06);
      pos[i * 3] += Math.sin(clock.elapsedTime * 0.7 + i) * dt * 0.02;
      if (pos[i * 3 + 1] > CUT_Y + 0.05) respawn(i);   // the cut: smoke stops here
    }
    pGeo.attributes.position.needsUpdate = true;
    renderer.render(scene, camera);
    raf = requestAnimationFrame(tick);
  }
  tick();

  /* visibility + resize hygiene */
  new IntersectionObserver((en) => {
    if (en[0].isIntersecting) { if (!raf) { clock.getDelta(); raf = requestAnimationFrame(tick); } }
    else { cancelAnimationFrame(raf); raf = 0; }
  }, { threshold: 0.02 }).observe(container);
  new ResizeObserver(() => {
    renderer.setSize(W(), H());
    camera.aspect = W() / H();
    camera.updateProjectionMatrix();
  }).observe(container);
}
