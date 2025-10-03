#!/bin/bash

# Build and deployment script for Project Sentinel React Dashboard

echo "🛡️  Project Sentinel Dashboard - Build & Deploy Script"
echo "=================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm are available"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Build the project
echo "🔨 Building the project..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Build completed successfully"

# Check if build directory exists
if [ ! -d "build" ]; then
    echo "❌ Build directory not found"
    exit 1
fi

echo "📁 Build files created in ./build/"

# Optional: Copy build files to deployment directory
# Uncomment and modify the following lines if you want to deploy to a specific directory
# DEPLOY_DIR="/path/to/your/deployment/directory"
# if [ -d "$DEPLOY_DIR" ]; then
#     echo "🚀 Deploying to $DEPLOY_DIR..."
#     cp -r build/* "$DEPLOY_DIR/"
#     echo "✅ Deployment completed"
# else
#     echo "⚠️  Deployment directory $DEPLOY_DIR not found"
# fi

echo ""
echo "🎉 Project Sentinel Dashboard is ready!"
echo ""
echo "To start the development server:"
echo "  npm start"
echo ""
echo "To serve the production build:"
echo "  npx serve -s build"
echo ""
echo "Build files are located in: ./build/"
echo "=================================================="