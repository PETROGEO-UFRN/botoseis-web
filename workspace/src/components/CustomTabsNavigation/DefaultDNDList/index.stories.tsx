import type { Meta, StoryObj } from '@storybook/react';

import DefaultDNDList from '.';

const getMockItems = () => Array(2).fill({}).map((_, index) => (
  {
    id: index,
    name: `ITEM ${index}`,
  }
))

// More on how to set up stories at: https://storybook.js.org/docs/writing-stories#default-export
const meta = {
  title: 'DefaultDNDList',
  component: DefaultDNDList,
  argTypes: {
    children: {
      description: "List of components that can be drag. Must be compatible with `@dnd-kit/core` like `CustomTab`",
    },
    items: {
      control: "array",
      description: "List of items, usualy from a `useState`",
    },
    setItems: {
      description: "setState to the items list state",
    },
    orientation: {
      control: 'select',
      options: ['vertical', 'horizontal'],
      description: 'Orientation of list, controls dragable direction. avaliable options: `horizontal`, `vertical`',
      defaultValue: "horizontal",
    },
  },
  tags: ['autodocs'],
} satisfies Meta<typeof DefaultDNDList>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Tab: Story = {
  args: {
    children: (
      <h1>This component is not visual. Check it's docs</h1>
    ),
    items: getMockItems(),
    setItems: () => undefined
  },
};
