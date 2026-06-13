import React, { useRef, useEffect } from 'react';
import { drawGraph, MAX_VALUE } from '../utils/drawGraph';

const Graph = ({ r, points, onGraphClick }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    drawGraph(canvas, r, points);
  }, [r, points]);

  const handleClick = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const width = canvas.width;

    const padding = 20;
    const pixelsPerUnit = (width / 2 - padding) / MAX_VALUE;

    const centerX = width / 2;
    const centerY = canvas.height / 2;

    const xClick = e.clientX - rect.left;
    const yClick = e.clientY - rect.top;

    const xGraph = (xClick - centerX) / pixelsPerUnit;
    const yGraph = (centerY - yClick) / pixelsPerUnit;

    onGraphClick(xGraph, yGraph);
  };

  return (
      <div className="graph-container"  >
        <canvas
            ref={canvasRef}
            width={500}
            height={500}
            onClick={handleClick}
            className="graph-canvas"
        />
      </div>
  );
};

export default Graph;