import type { Meta, StoryObj } from '@storybook/react';
import { action } from '@storybook/addon-actions';

import FileUploadDialog from './';

type Story = StoryObj<typeof FileUploadDialog>;

const meta: Meta<Story> = {
  title: 'Components/FileSelector/FileUploadDialog',
  component: FileUploadDialog,
};

export default meta;

export const Default: Story = {
  args: {
    open: true,
    setOpen: () => action('Clicked open!'),
    uploadNewFile: () => action('Shall upload'),
  }
};
