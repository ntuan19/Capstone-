function celebrate() {
    // create a canvas element and append it to the document
    const canvas = document.createElement('canvas');
    document.body.appendChild(canvas);
  
    // set canvas size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  
    // create a new fireworks object and launch it
    const fireworks = new Fireworks(canvas);
    fireworks.launch();
  }
  