import { useEffect, useRef } from 'react';

export function SpaceBackground() {
  const canvasRef = useRef(null);
  const particlesRef = useRef([]);
  const offsetRef = useRef(0);
  const rafRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initializeParticles();
    };

    const initializeParticles = () => {
      particlesRef.current = [];
      const particleCount = Math.floor((canvas.width * canvas.height) / 8000);

      for (let i = 0; i < particleCount; i++) {
        particlesRef.current.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          radius: Math.random() * 1.5,
          opacity: Math.random() * 0.7 + 0.3,
          vx: (Math.random() - 0.5) * 0.3,
          vy: (Math.random() - 0.5) * 0.3,
        });
      }
    };

    const drawBackground = () => {
      const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
      gradient.addColorStop(0, '#0B1220');
      gradient.addColorStop(0.5, '#14181B');
      gradient.addColorStop(1, '#0D1015');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    };

    const updateParticles = () => {
      particlesRef.current.forEach((particle) => {
        particle.x += particle.vx;
        particle.y += particle.vy;

        if (particle.x < 0) particle.x = canvas.width;
        if (particle.x > canvas.width) particle.x = 0;
        if (particle.y < 0) particle.y = canvas.height;
        if (particle.y > canvas.height) particle.y = 0;

        particle.opacity += (Math.random() - 0.5) * 0.02;
        particle.opacity = Math.max(0.1, Math.min(0.8, particle.opacity));

        ctx.fillStyle = `rgba(232, 236, 238, ${particle.opacity})`;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        ctx.fill();

        if (particle.opacity > 0.6) {
          ctx.fillStyle = `rgba(79, 143, 232, ${particle.opacity * 0.3})`;
          ctx.beginPath();
          ctx.arc(particle.x, particle.y, particle.radius * 2.5, 0, Math.PI * 2);
          ctx.fill();
        }
      });
    };

    const drawNebula = () => {
      const time = offsetRef.current * 0.0001;

      const nebula1 = ctx.createRadialGradient(
        canvas.width * 0.3 + Math.sin(time) * 100,
        canvas.height * 0.4 + Math.cos(time * 0.7) * 100,
        0,
        canvas.width * 0.3,
        canvas.height * 0.4,
        400
      );
      nebula1.addColorStop(0, 'rgba(79, 143, 232, 0.15)');
      nebula1.addColorStop(0.5, 'rgba(79, 143, 232, 0.05)');
      nebula1.addColorStop(1, 'rgba(79, 143, 232, 0)');
      ctx.fillStyle = nebula1;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const nebula2 = ctx.createRadialGradient(
        canvas.width * 0.7 + Math.sin(time * 0.6) * 80,
        canvas.height * 0.6 + Math.cos(time * 0.8) * 80,
        0,
        canvas.width * 0.7,
        canvas.height * 0.6,
        350
      );
      nebula2.addColorStop(0, 'rgba(76, 174, 140, 0.12)');
      nebula2.addColorStop(0.5, 'rgba(76, 174, 140, 0.04)');
      nebula2.addColorStop(1, 'rgba(76, 174, 140, 0)');
      ctx.fillStyle = nebula2;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    };

    const animate = () => {
      drawBackground();
      drawNebula();
      updateParticles();
      offsetRef.current++;
      rafRef.current = requestAnimationFrame(animate);
    };

    resizeCanvas();
    animate();

    window.addEventListener('resize', resizeCanvas);

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
      }
    };
  }, []);

  return (
    <div className="space-background">
      <canvas ref={canvasRef} className="space-background-canvas" />
      <div className="space-background-overlay" />
    </div>
  );
}
