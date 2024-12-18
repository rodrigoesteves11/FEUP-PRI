import React, { useEffect, useState } from "react";
import { styled, keyframes } from "@mui/system";
import image from "../common/BioFinder (4).png";

const float = keyframes`
  0% {
    transform: translateY(-1000px) rotate(0deg);
    opacity: 0.5;
    border-radius: 0;
  }
  100% {
    transform: translateY(0px) rotate(720deg);
    opacity: 0;
    border-radius: 50%;
  }
`;

const BackgroundContainer = styled("div")({
  position: "fixed",
  top: 0,
  left: 0,
  width: "100%",
  height: "100%",
  overflow: "hidden",
  zIndex: -1
});

const AnimatedImage = styled("img")<{ duration: number; delay: number; size: number; left: string }>(
  ({ duration, delay, size, left }) => ({
    position: "absolute",
    bottom: `-${size}px`,
    left: left,
    width: `${size}px`,
    height: `${size}px`,
    objectFit: "cover",
    animation: `${float} ${duration}s linear infinite`,
    animationDelay: `${delay}s`,
    pointerEvents: "none", 
  })
);

const imageUrls = [image];

const getRandom = (min: number, max: number) => Math.random() * (max - min) + min;

const AnimatedBackground: React.FC = () => {
  const [images, setImages] = useState<
    { id: number; url: string; duration: number; delay: number; size: number; left: string }[]
  >([]);

  useEffect(() => {
    const interval = setInterval(() => {
      const newImage = {
        id: Date.now(),
        url: imageUrls[Math.floor(Math.random() * imageUrls.length)],
        duration: getRandom(20, 40), // Duração da animação em segundos
        delay: getRandom(0, 0), // Atraso inicial em segundos
        size: getRandom(40, 150), // Tamanho da imagem em pixels
        left: `${getRandom(-50, 150)}%`, // Posição horizontal
      };
      setImages((prev) => [...prev, newImage]);

      
      setTimeout(() => {
        setImages((prev) => prev.filter((img) => img.id !== newImage.id));
      }, newImage.duration * 500);
    }, 500);

    return () => clearInterval(interval);
  }, []);

  return (
    <BackgroundContainer>
      {images.map((image) => (
        <AnimatedImage
          key={image.id}
          src={image.url}
          alt="Animated"
          duration={image.duration}
          delay={image.delay}
          size={image.size}
          left={image.left}
        />
      ))}
    </BackgroundContainer>
  );
};

export default AnimatedBackground;
