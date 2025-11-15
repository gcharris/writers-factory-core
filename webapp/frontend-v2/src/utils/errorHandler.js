/**
 * Friendly error message handler for Writers Factory.
 * Converts technical errors into user-friendly messages.
 */

export function getFriendlyErrorMessage(error, context = {}) {
  // Network errors
  if (error.message?.includes('fetch') || error.message?.includes('network') || error.message?.includes('Failed to fetch')) {
    return {
      title: "Connection Error",
      message: "Couldn't connect to the Writers Factory backend. Make sure it's running at localhost:8000.",
      action: "Check that you started the backend with: python webapp/backend/simple_app.py",
      icon: "🔌"
    };
  }

  // 404 errors
  if (error.status === 404 || error.message?.includes('404')) {
    if (context.type === 'scene') {
      return {
        title: "Scene Not Found",
        message: "The scene you're looking for doesn't exist. It may have been deleted.",
        action: "Try refreshing the page or selecting a different scene.",
        icon: "📄"
      };
    }
    return {
      title: "Not Found",
      message: "The resource you requested couldn't be found.",
      action: "Try refreshing the page or checking your request.",
      icon: "❓"
    };
  }

  // 500 errors
  if (error.status === 500 || error.message?.includes('500')) {
    return {
      title: "Server Error",
      message: "Something went wrong on the server. This is usually temporary.",
      action: "Try refreshing the page. If the problem persists, check the backend logs.",
      icon: "⚠️"
    };
  }

  // API key errors
  if (error.message?.includes('API key') || error.message?.includes('authentication') || error.message?.includes('Unauthorized')) {
    return {
      title: "API Key Missing or Invalid",
      message: "Your AI model API key is missing or invalid.",
      action: "Go to Settings > API Keys and add your API key for the model you're using.",
      icon: "🔑"
    };
  }

  // Ollama errors
  if (error.message?.includes('Ollama') || error.message?.includes('11434')) {
    return {
      title: "Ollama Not Running",
      message: "Ollama isn't running or isn't accessible. Local models won't work without it.",
      action: "Start Ollama by running 'ollama serve' in your terminal, or install from ollama.ai",
      icon: "🦙"
    };
  }

  // Model errors
  if (error.message?.includes('model') && context.type === 'generation') {
    return {
      title: "AI Generation Failed",
      message: "The AI model couldn't generate content. This might be due to API limits, invalid keys, or model unavailability.",
      action: "Check your API keys, try a different model, or enable Economy Mode to use local models.",
      icon: "🤖"
    };
  }

  // Rate limit errors
  if (error.message?.includes('rate limit') || error.message?.includes('429')) {
    return {
      title: "Rate Limit Exceeded",
      message: "You've made too many requests to the AI model. The API has temporary limits.",
      action: "Wait a few minutes before trying again, or switch to a different model.",
      icon: "⏱️"
    };
  }

  // Timeout errors
  if (error.message?.includes('timeout') || error.message?.includes('timed out')) {
    return {
      title: "Request Timeout",
      message: "The operation took too long and timed out.",
      action: "Try again with a shorter text, or check your internet connection.",
      icon: "⏰"
    };
  }

  // Generic error
  return {
    title: "Something Went Wrong",
    message: error.message || "An unexpected error occurred.",
    action: "Try refreshing the page. If the problem persists, check the browser console for details.",
    icon: "❌"
  };
}

/**
 * Display friendly error with toast notification
 */
export function showFriendlyError(error, toast, context = {}) {
  const friendly = getFriendlyErrorMessage(error, context);

  toast.error(
    `${friendly.icon} ${friendly.title}: ${friendly.message}${friendly.action ? ' — ' + friendly.action : ''}`,
    { duration: 6000 }
  );
}
