import React from 'react';
import ReactDOM from 'react-dom/client';

import FloatingLines from './src/FloatingLines';



function FloatingLinesApp() {
    return (
        // height:'100%' en vez de 'auto': el padre (#floating-lines-root)
        // ahora fija su propia altura en floating-theme.css (100vh/100lvh)
        // como fondo global fijo; este wrapper debe heredar esa altura al
        // 100%, no calcularla por su contenido, o el canvas queda a 0px.
        <div style={{ width: '100%', height: '100%', position: 'relative' }}>
            <FloatingLines
                enabledWaves={["top","middle","bottom"]}
                lineCount={8}
                lineDistance={8}
                bendRadius={8}
                bendStrength={-2}
                interactive
                parallax={true}
                animationSpeed={1}
                
                 linesGradient={["#027177", "#1f1f1f", "#1f1f1f"]}

            />
        </div>
    );
}

const floatingLinesRoot = document.getElementById('floating-lines-root');

if (floatingLinesRoot) {
    ReactDOM.createRoot(floatingLinesRoot).render(
        <React.StrictMode>
            <FloatingLinesApp />
        </React.StrictMode>
    );
}










