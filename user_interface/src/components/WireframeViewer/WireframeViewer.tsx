"use client";

import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import * as THREE from "three";
import { useMemo, useState } from "react";
import { Box, Typography, IconButton } from "@mui/material";
import GridOnIcon from "@mui/icons-material/GridOn";
import GridOffIcon from "@mui/icons-material/GridOff";

const labelColors: Record<number, string | null> = {
    0: "#e6194b",  // Rot
    1: "#3cb44b",  // Grün
    2: "#ffe119",  // Gelb
    3: "#4363d8",  // Blau
    4: "#f58231",  // Orange
    5: "#911eb4",  // Violett
    6: "#42d4f4",  // Cyan
    7: "#f032e6",  // Pink
    8: "#bfef45",  // Hellgrün
    9: null        // Kein Label oder transparent
};

interface WireframeViewerProps {
    fileUrl: string;
    features: number[][];
    predictedLabels: number[];
}

export default function WireframeViewer({ fileUrl, features, predictedLabels }: WireframeViewerProps) {
    const [isWireframe, setIsWireframe] = useState(true);

    const toggleWireframe = () => {
        setIsWireframe((prev) => !prev);
    };

    return (
        <Box
            sx={{
                width: "40vw",
                minWidth: "300px",
                height: "40vw",
                maxHeight: "400px",
                borderRadius: 2,
                overflow: "hidden",
                bgcolor: "#787474",
                boxShadow: "3px 3px 10px rgba(0,0,0,0.2)",
                margin: "auto",
            }}
        >
            <Box
                sx={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    padding: "8px 16px",
                    backgroundColor: "#787474",
                    position: "relative"
                }}
            >
                <Typography
                    align="center"
                    variant="h6"
                    sx={{ fontWeight: "bold", color: "white" }}
                >
                    Model Viewer
                </Typography>
                <IconButton
                    onClick={toggleWireframe}
                    color="primary"
                    size="small"
                    sx={{ position: "absolute", right: 8 }}
                >
                    {isWireframe ? <GridOffIcon /> : <GridOnIcon />}
                </IconButton>
            </Box>
            <Canvas
                camera={{ position: [100, 100, 100], fov: 45 }}
                shadows
                style={{ background: "whitesmoke", width: "100%", height: "90%" }}
            >
                <ambientLight intensity={1} color={"#ffffff"} />
                <spotLight position={[15, 30, 15]} intensity={1.0} color={"#ffffff"} angle={0.5} penumbra={0.5} />
                <directionalLight position={[-20, 20, 10]} intensity={0.7} color={"#f0f0f0"} />
                <pointLight position={[-15, -15, -15]} intensity={0.4} color={"#ff7820"} />
                <hemisphereLight groundColor={"#444444"} intensity={0.3} />

                {fileUrl && <WireframeSTLMesh fileUrl={fileUrl} isWireframe={isWireframe} />}
                {features && predictedLabels && (
                    <LabeledVertices features={features} predictedLabels={predictedLabels} />
                )}
                <OrbitControls />
            </Canvas>
        </Box>
    );
}

function WireframeSTLMesh({ fileUrl, isWireframe }: { fileUrl: string, isWireframe: boolean }) {
    const geometry = useLoader(STLLoader, fileUrl) as THREE.BufferGeometry;

    return (
        <mesh>
            <primitive object={geometry} attach="geometry" />
            <meshStandardMaterial
                color="#ff7820"
                wireframe={isWireframe}
                opacity={1}
                transparent={false}
                roughness={0.3}
                metalness={0.5}
            />
        </mesh>
    );
}

function LabeledVertices({ features, predictedLabels }: { features: number[][]; predictedLabels: number[] }) {
    const vertices = useMemo(() => {
        const result = [];
        for (let i = 0; i < features.length; i++) {
            const label = predictedLabels[i];
            if (label === 9 || labelColors[label] == null) continue;
            const position = new THREE.Vector3(...features[i]);
            const color = labelColors[label]!;
            result.push({ position, color });
        }
        return result;
    }, [features, predictedLabels]);

    if (!vertices.length) return null;

    return (
        <>
            {vertices.map((v, i) => (
                <mesh key={i} position={v.position.toArray()}>
                    <sphereGeometry args={[2, 16, 16]} />
                    <meshStandardMaterial color={v.color} />
                </mesh>
            ))}
        </>
    );
}

