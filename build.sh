#!/bin/bash

# Build script for deployment
echo "Building React frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Copying build files to Flask static directory..."
cp -r frontend/build/* .

echo "Build completed!"
