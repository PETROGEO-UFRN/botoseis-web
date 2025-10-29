// *** set function o window to make it available on bokeh js callback declared on server-side, running on client-side
window.finishLoading = (tagsToStop) => {
  // *** prevents infinity loop
  if (tagsToStop.length === 0) return;

  tagsToStop.forEach(tag => {
    const loadingIconHTMLId = `#loading-${tag}-icon`

    try {
      const loadingIcon = document.querySelector(loadingIconHTMLId)
      const isLoading = loadingIcon.classList.contains("is-loading")
      if (isLoading)
        loadingIcon.classList.toggle("is-loading")
    } catch (error) {
      // ! Currently trigger on gain type. Not a major issue
      console.error(`Error stopping loading icon for tag: ${tag}`, error)
    }
  });
}
