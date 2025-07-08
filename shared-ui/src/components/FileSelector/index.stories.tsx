import type { Meta, StoryObj } from '@storybook/react';
import { action } from '@storybook/addon-actions';

import FileSelector from './';

type Story = StoryObj<typeof FileSelector>;

const meta: Meta<Story> = {
  title: 'Components/FileSelector',
  component: FileSelector,
};

const mockFileLinks: Array<IfileLink> = [
  {
    id: 1,
    name: 'Arquivo 1',
    data_type: '',
    projectId: 1,
    datasetId: 1,
  },
  {
    id: 2,
    name: 'Arquivo 2',
    data_type: '',
    projectId: 1,
    datasetId: 1,
  },
]

export default meta;

export const Default: Story = {
  args: {
    fileLinks: mockFileLinks,
    uploadNewFile: () => action('Shall upload'),
    selectedFileLinkId: 1,
    onSubmitFileLinkUpdate: () => action('Shall update selected file')
  }
};
