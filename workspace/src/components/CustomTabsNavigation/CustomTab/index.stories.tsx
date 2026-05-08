import type { Meta, StoryObj } from '@storybook/react';

import CustomTab from '.';

// More on how to set up stories at: https://storybook.js.org/docs/writing-stories#default-export
const meta = {
  title: 'CustomTab',
  component: CustomTab,
  decorators: [
    (Story) => (
      <div style={{ height: '500px' }}>
        <Story />
      </div>
    ),
  ],
  argTypes: {
    value: {
      control: "number",
      description: "Key used to interactivity (drag and drop and tab selection)",
    },
    label: {
      control: "text",
      description: "Label to the Tab and it's tooltip",
    },
    $color: {
      control: 'select',
      options: ['primary', 'seconday', 'white'],
      description: 'Color pattern from theme to use, avaliable options: `primary`, `seconday`, `white`',
      defaultValue: "primary",
    },
    $orientation: {
      control: 'select',
      options: ['vertical', 'horizontal'],
      description: 'Orientation from parent container list. avaliable options: `horizontal`, `vertical`',
      defaultValue: "horizontal",
    },
  },
  tags: ['autodocs'],
} satisfies Meta<typeof CustomTab>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Tab: Story = {
  args: {
    value: 1,
    label: "Tab title",
    $color: 'primary',
    $orientation: 'horizontal'
  },
};
