import type { Preview } from '@storybook/react';
import { ThemeProvider, CssBaseline, createTheme } from '@mui/material';

const theme = createTheme();

const StoryWrapper = (Story, context) => {
  const isSmallBox = context.parameters?.isSmallBox ?? false;

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {isSmallBox ? (
        <div style={{ maxWidth: 512 }}>
          <Story />
        </div>
      ) : (
        <Story />
      )}
    </ThemeProvider>
  );
};

const preview: Preview = {
  decorators: [StoryWrapper],
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};

export default preview;
