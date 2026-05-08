import type { Meta, StoryObj } from '@storybook/react';
import { action } from '@storybook/addon-actions';

import DeleteButton from './';

type Story = StoryObj<typeof DeleteButton>;

const meta: Meta<Story> = {
  title: 'Components/DeleteButton',
  component: DeleteButton,
};

export default meta;

export const Default: Story = {
  args: {
    onRemove: () => action('Clicked delete!'),
    size: 'large',
  },
  decorators: [
    (Story) => (
      <div style={{ padding: "0 64px" }}>
        <Story />
      </div>
    ),
  ],
};
