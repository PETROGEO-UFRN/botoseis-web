import type { Meta, StoryObj } from '@storybook/react';

import ProjectTab from '.';

// More on how to set up stories at: https://storybook.js.org/docs/writing-stories#default-export
const meta = {
  title: 'ProjectTab',
  component: ProjectTab,
  decorators: [
    (Story) => (
      <div style={{ height: '500px' }}>
        <Story />
      </div>
    ),
  ],
  tags: ['autodocs'],
} satisfies Meta<typeof ProjectTab>;

export default meta;

type Story = StoryObj<typeof meta>;

export const RegularProjectTab: Story = {
  args: {},
};
