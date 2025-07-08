import type { Meta, StoryObj } from '@storybook/react'
import { useState } from 'react'

import CustomTabsNavigation from '.'
import DefaultDNDList from '../DefaultDNDList'

// More on how to set up stories at: https://storybook.js.org/docs/writing-stories#default-export
const meta = {
  title: 'CustomTabsNavigation',
  component: CustomTabsNavigation,
  decorators: [
    (Story) => (
      <div style={{ height: '500px' }}>
        <Story />
      </div>
    ),
  ],
  argTypes: {
    tabs: {
      control: "array",
      description: "List of tabs, usualy from a `useState`",
    },
    setTabs: {
      description: "setState to the tabs list state",
    },
    selectedTabId: {
      control: "number",
      description: "Key the tab selected to display. Necessary to drag and drop feature.",
    },
    setSelectedTabId: {
      description: "setState to `selectedTab` state",
    },
    CustomDndContext: {
      description: `Component to provide drag and drop context. By default will
                    render the the children without doing anything`,
    },
    color: {
      control: 'select',
      options: ['primary', 'seconday', 'white'],
      description: 'Color pattern from theme to use, avaliable options: `primary`, `seconday`, `white`',
      defaultValue: "primary",
    },
    orientation: {
      control: 'select',
      options: ['vertical', 'horizontal'],
      description: 'Orientation from parent container list. avaliable options: `horizontal`, `vertical`',
      defaultValue: "horizontal",
    },
  },
  tags: ['autodocs'],
} satisfies Meta<typeof CustomTabsNavigation>;

export default meta;

type Story = StoryObj<typeof meta>;

function getTabs(amount: number) {
  const tabs = Array(amount).fill({}).map((_, index) => (
    {
      id: index,
      name: `tab ${index}`,
    }
  ))
  if (tabs.length > 2)
    tabs[2].name = tabs[2].name.concat(
      " ",
      "have a really really really long name"
    )
  return tabs
}

export const FewTabs: Story = {
  args: {
    selectedTabId: 1,
    tabs: getTabs(5),
    setSelectedTabId: () => undefined,
  },
};

export const ManyTabs: Story = {
  args: {
    selectedTabId: 1,
    tabs: getTabs(30),
    setSelectedTabId: () => undefined,
  },
};

export const DragableTabs = () => {
  const [tabs, setTabs] = useState(getTabs(8))
  return (
    <div style={{ height: '500px' }}>
      <CustomTabsNavigation
        selectedTabId={1}
        tabs={tabs}
        setTabs={setTabs}
        setSelectedTabId={() => undefined}
        CustomDndContext={DefaultDNDList}
      />
    </div>
  )
};
