let scene, camera, renderer, bars, analyser, dataArray, audio, audioContext;

// Audio setup
function setupAudio() {
  audio = new Audio('BarerleyThere.mp3'); // Ensure file is in project folder
  audio.crossOrigin = 'anonymous'; // For CORS if track is external
  audioContext = new AudioContext();
  const source = audioContext.createMediaElementSource(audio);
  analyser = audioContext.createAnalyser();
  analyser.fftSize = 256;
  dataArray = new Uint8Array(analyser.frequencyBinCount);
  source.connect(analyser);
  analyser.connect(audioContext.destination);

  // Error handling for audio loading
  audio.addEventListener('error', () => {
    showError('Failed to load audio file. Check path or file format.');
  });
}

// Three.js setup
function init() {
  scene = new THREE.Scene();

  // Orthographic camera for isometric (no perspective distortion)
  const aspect = window.innerWidth / window.innerHeight;
  const zoom = 30; // Adjust for scene size
  camera = new THREE.OrthographicCamera(-zoom * aspect, zoom * aspect, zoom, -zoom, 0.1, 1000);

  // Isometric position: 45° yaw, ~35° pitch
  const distance = 100;
  camera.position.set(distance * Math.sin(Math.PI / 8), distance * Math.sin(Math.PI / -8), distance * Math.cos(Math.PI / 4));
  camera.lookAt(0, 0, 0);

  renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  // Create bar grid
  bars = [];
  const geometry = new THREE.BoxGeometry(1.5, 1.5, 1); // Building-like bars
  for (let x = -12; x <= 12; x += 3) {
    for (let y = -12; y <= 12; y += 3) {
      const material = new THREE.MeshBasicMaterial({ color: 0xffffff });
      const bar = new THREE.Mesh(geometry, material);
      bar.position.set(x, y, 2 + Math.random() * 10); // Varied base heights
      scene.add(bar);
      bars.push(bar);
    }
  }

  window.addEventListener('resize', () => {
    const aspect = window.innerWidth / window.innerHeight;
    camera.left = -zoom * aspect;
    camera.right = zoom * aspect;
    camera.top = zoom;
    camera.bottom = -zoom;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
}

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  analyser.getByteFrequencyData(dataArray);
  bars.forEach((bar, i) => {
    const freqIndex = (i % (dataArray.length - 8)) + 8; // Skip first 8 bins
    const freq = dataArray[freqIndex] / 130; // Livelier scaling
    bar.scale.z = 1 + freq * 20; // Taller, dynamic heights
    bar.position.z = bar.scale.z / 2; // Keep base grounded
    bar.material.color.setHSL((freq * 0.3 + 0.5) % 1, 0.7, 0.5); // Neon cyan/pink/purple
  });
  renderer.render(scene, camera);
}

// Show error message
function showError(message) {
  const errorDiv = document.getElementById('errorMessage');
  errorDiv.textContent = message;
  errorDiv.style.display = 'block';
}

// Start everything on button click
const startButton = document.getElementById('startButton');
startButton.addEventListener('click', () => {
  startButton.style.display = 'none';
  try {
    setupAudio();
    init();
    audio.play().then(() => {
      audioContext.resume().then(() => {
        animate();
      }).catch(err => showError('Audio context failed: ' + err.message));
    }).catch(err => showError('Audio playback failed: ' + err.message));
  } catch (err) {
    showError('Setup failed: ' + err.message);
  }
});