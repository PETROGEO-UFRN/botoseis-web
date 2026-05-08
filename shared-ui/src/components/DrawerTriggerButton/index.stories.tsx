import type { Meta, StoryObj } from '@storybook/react';
import DrawerTriggerButton from './';
import { useState } from 'react';
import AddIcon from '@mui/icons-material/Add';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';

const meta: Meta<typeof DrawerTriggerButton> = {
  title: 'Components/DrawerTriggerButton',
  component: DrawerTriggerButton,
  argTypes: {
    $top: {
      control: 'text',
      description: 'Distance from top (e.g. "16px")',
    },
    $bottom: {
      control: 'text',
      description: 'Distance from bottom (e.g. "16px")',
    },
    $left: {
      control: 'text',
      description: 'Distance from left (e.g. "16px")',
    },
    $right: {
      control: 'text',
      description: 'Distance from right (e.g. "16px")',
    },
  },
  args: {
    $top: undefined,
    $bottom: '16px',
    $left: undefined,
    $right: '16px',
  },
};

export default meta;

type Story = StoryObj<typeof DrawerTriggerButton>;

export const Default: Story = {
  render: (args) => {
    const [isOpen, setIsOpen] = useState(false);

    return (
      <div style={{ padding: 32 }}>
        <DrawerTriggerButton
          startIcon={<AddIcon />}
          endIcon={<ArrowForwardIosIcon />}
          {...args}
          setIsOpen={setIsOpen}
        >
          Abrir Drawer
        </DrawerTriggerButton>

        {isOpen && (
          <div
            style={{
              marginTop: 16,
              padding: 12,
              backgroundColor: '#eee',
              borderRadius: 8,
              maxWidth: 300,
            }}
          >
            🔓 O Drawer foi aberto!
          </div>
        )}
      </div>
    );
  },
};
