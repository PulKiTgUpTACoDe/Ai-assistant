# AI Agent Frontend

A modern, responsive web interface for the AI Agent built with Next.js 15, TypeScript, and Tailwind CSS.

## 🌟 Features

- **Modern UI/UX**

  - Responsive design with mobile-first approach
  - Dark/Light theme support
  - Smooth animations with Framer Motion
  - Beautiful UI components using Radix UI

- **Chat Interface**

  - Real-time chat with AI agent
  - Message history persistence
  - Auto-scrolling chat window
  - Loading states and error handling
  - Markdown support for messages

- **Session Management**

  - Multiple chat sessions
  - Automatic session naming based on first message
  - Session renaming and deletion
  - Persistent session storage

- **Authentication**

  - Secure authentication with Clerk
  - Protected API routes
  - User session management
  - Query limit for non-authenticated users

- **API Integration**
  - Seamless communication with Python backend
  - WebSocket support for real-time updates
  - Error handling and retry mechanisms
  - Type-safe API calls

## 🚀 Getting Started

### Prerequisites

- Node.js 18 or higher
- npm, yarn, or pnpm
- Python backend running (see backend README)

### Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd ai-agent-frontend
   ```

2. **Install Dependencies**

   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Environment Setup**
   Create a `.env.local` file with the following variables:

   ```
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_key
   CLERK_SECRET_KEY=your_clerk_secret
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   ```

4. **Database Setup**

   ```bash
   npx prisma generate
   npx prisma db push
   ```

5. **Start Development Server**

   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

   Open [http://localhost:3000](http://localhost:3000) to see the application.

## 🛠️ Development

### Project Structure

```
ai-agent-frontend/
├── app/              # Next.js app directory
├── components/       # React components
│   ├── ui/          # Reusable UI components
│   └── ...          # Feature-specific components
├── lib/             # Utility functions and hooks
├── prisma/          # Database schema and migrations
├── public/          # Static assets
└── styles/          # Global styles
```

### Key Technologies

- **Framework**: Next.js 15
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI
- **State Management**: React Context
- **Authentication**: Clerk
- **Database**: Prisma with PostgreSQL
- **Animation**: Framer Motion
- **API Client**: Built-in fetch with type safety

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
