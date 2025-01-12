export default function PostCreateInjectedScripts() {
  const htmlContent = `
    <script id="vs" type="x-shader/x-vertex">
    // Vertex shader code
    </script>
    <script id="fs" type="x-shader/x-fragment">
    // Fragment shader code
    </script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/three.js/84/three.js'></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/three.js/84/three.min.js'></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/three.js/84/controls/OrbitControls.js'></script>
    <script>
    window.onload = () => {
      if (!window.Webgl) {
        class Webgl {
          constructor() {
            this.vertShader = document.getElementById("vs").textContent;
            this.fragShader = document.getElementById("fs").textContent;
            this.setProps();
            this.init();
          }
          init() {
            this.scene = new THREE.Scene();
            this.camera = new THREE.PerspectiveCamera(45, this.props.width / this.props.height, this.props.near, this.props.far);
            this.camera.position.set(10, 10, -10);
            this.camera.lookAt(this.scene.position);
            this.renderer = new THREE.WebGLRenderer({
              antialias: true,
              alpha: true
            });
            this.renderer.setPixelRatio(1.5);
            this.renderer.setClearColor(0xb7d3dc, 0.3);
            this.renderer.setSize(this.props.width, this.props.height);
            this.div = document.getElementById("wrapper");
            this.div.appendChild(this.renderer.domElement);
            this.obj = new Obj(this);
            this.render();
            var control = new THREE.OrbitControls(this.camera, this.renderer.domElement);
          }
          setProps() {
            var width = document.body.clientWidth;
            var height = window.innerHeight;
            var aspect = width / height;
            this.props = {
              width: width,
              height: height,
              aspect: aspect,
              left: -width / 2,
              right: width / 2,
              top: height / 2,
              bottom: -height / 2,
              near: 0.1,
              far: 10000
            };
          }
          resize() {
            this.setProps();
            this.renderer.setSize(this.props.width, this.props.height);
            this.camera.aspect = this.props.width / this.props.height;
            this.camera.updateProjectionMatrix();
          }
          render() {
            this.obj.uniforms.uTick.value += 1;
            this.renderer.render(this.scene, this.camera);
            requestAnimationFrame(this.render.bind(this));
          }
        }
        window.Webgl = Webgl;
      }
      if (!window.Obj) {
        class Obj {
          constructor(webgl) {
            this.webgl = webgl;
            this.init();
          }
          paramFunc() {
            return new THREE.Vector3(0, 0, 0);
          }
          init() {
            var g = new THREE.ParametricBufferGeometry(this.paramFunc, 100, 100);
            const uvArray = [];
            for (let i = 0; i < 100; i++) {
              var _u = i / 99;
              for (let j = 0; j < 100; j++) {
                var _v = j / 99;
                uvArray.push(_u, _v);
              }
            }
            this.uniforms = {
              uTick: { type: "f", value: 0 }
            };
            var m = new THREE.ShaderMaterial({
              vertexShader: this.webgl.vertShader,
              fragmentShader: this.webgl.fragShader,
              uniforms: this.uniforms,
              side: THREE.DoubleSide,
              shading: THREE.FlatShading
            });
            var mesh = new THREE.Mesh(g, m);
            this.webgl.scene.add(mesh);
          }
        }
        window.Obj = Obj;
      }
      var webgl = new Webgl();
      window.onresize = () => {
        webgl.resize();
      };
    };
    </script>
  `;

  const wrapper = document.createElement('div');
  wrapper.innerHTML = htmlContent;
  document.body.appendChild(wrapper);

  // Execute scripts
  const scripts = wrapper.querySelectorAll('script');
  scripts.forEach(script => {
    const newScript = document.createElement('script');
    if (script.src) {
      newScript.src = script.src;
    } else {
      newScript.type = script.type;
      newScript.textContent = script.textContent;
    }
    document.body.appendChild(newScript);
  });
}