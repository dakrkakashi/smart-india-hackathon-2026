#!/bin/bash

# Magic UI Components Installation Script for Pralay Frontend

echo "🎨 Installing Magic UI Components for Pralay..."

# Navigate to frontend directory
cd "$(dirname "$0")/../frontend"

echo "📦 Installing UI Components..."

# Components
npx shadcn@latest add @magicui/shine-border -y
npx shadcn@latest add @magicui/confetti -y
npx shadcn@latest add @magicui/meteors -y
npx shadcn@latest add @magicui/animated-theme-toggler -y
npx shadcn@latest add @magicui/particles -y

echo "✨ Installing Text Animations..."

# Text Animations
npx shadcn@latest add @magicui/text-animate -y
npx shadcn@latest add @magicui/line-shadow-text -y
npx shadcn@latest add @magicui/number-ticker -y
npx shadcn@latest add @magicui/animated-gradient-text -y
npx shadcn@latest add @magicui/dia-text-reveal -y
npx shadcn@latest add @magicui/hyper-text -y
npx shadcn@latest add @magicui/scroll-based-velocity -y
npx shadcn@latest add @magicui/sparkles-text -y

echo "📱 Installing Device Mocks..."

# Device Mocks
npx shadcn@latest add @magicui/android -y

echo "🌈 Installing Backgrounds..."

# Backgrounds
npx shadcn@latest add @magicui/flickering-grid -y
npx shadcn@latest add @magicui/animated-grid-pattern -y
npx shadcn@latest add @magicui/dot-pattern -y
npx shadcn@latest add @magicui/hexagon-pattern -y
npx shadcn@latest add @magicui/floating-3d-particles -y

echo "🎭 Installing Community Components..."

# Community
npx shadcn@latest add @magicui/kinetic-text -y
npx shadcn@latest add @magicui/cool-mode -y
npx shadcn@latest add @magicui/interactive-hover-button -y
npx shadcn@latest add @magicui/glyph-matrix -y
npx shadcn@latest add @magicui/backlight -y

echo "✅ All Magic UI components installed successfully!"
echo "🚀 You can now use these components in your React components"
