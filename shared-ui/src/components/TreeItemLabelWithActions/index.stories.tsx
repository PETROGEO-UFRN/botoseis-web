import type { Meta, StoryObj } from '@storybook/react';
import { action } from '@storybook/addon-actions';

import { SimpleTreeView } from '@mui/x-tree-view';
import { TreeItem } from '@mui/x-tree-view';

import TreeItemLabelWithActions from './';

type Story = StoryObj<typeof TreeItemLabelWithActions>;

// *** Default story to show update option in action ***
interface ITreeItemLabelWithActionsStory {
  labelText?: string
  onUpdate?: undefined | (() => void)
}

function TreeItemLabelWithActionsStory({
  labelText = "Label",
  onUpdate = undefined,
}: ITreeItemLabelWithActionsStory) {
  return (
    <TreeItemLabelWithActions
      labelText={labelText}
      onRemove={() => action('Clicked delete!')}
      onUpdate={onUpdate}
    />
  )
}
// ***

const meta: Meta<typeof TreeItemLabelWithActions> = {
  title: 'Components/TreeItemLabelWithActions',
  component: TreeItemLabelWithActions,
};

export default meta;

export const Default: Story = {
  args: {
    labelText: 'Label',
    onRemove: () => action('Clicked delete!'),
  },
  parameters: {
    isSmallBox: true,
  },
};

export const WithUpdate: Story = {
  args: {
    labelText: 'Label',
    onRemove: () => action('Clicked delete!'),
    onUpdate: () => action('Clicked update!'),
  },
  parameters: {
    isSmallBox: true,
  },
};

export const OnTreeItemExamples: Story = {
  args: {
    labelText: 'Label',
    onRemove: () => action('Clicked delete!'),
  },
  parameters: {
    isSmallBox: true,
  },
  decorators: [
    (Story) => (
      <SimpleTreeView>
        <TreeItem
          itemId="1"
          label={<Story />}
        >
          <TreeItem
            itemId="2"
            label={<Story />}
          />
          <TreeItem
            itemId="3"
            label={<Story />}
          />
        </TreeItem>
      </SimpleTreeView>
    ),
  ],
}

export const OnTreeItemExamplesWithUpdate: Story = {
  parameters: {
    isSmallBox: true,
  },
  decorators: [
    (Story) => (
      <SimpleTreeView>
        <TreeItem
          itemId="1"
          label={
            <TreeItemLabelWithActionsStory
              labelText='Label 1'
              onUpdate={() => action('Clicked update!')}
            />
          }
        >
          <TreeItem
            itemId="2"
            label={
              <TreeItemLabelWithActionsStory
                labelText='Label 2'
                onUpdate={() => action('Clicked update!')}
              />
            }
          />
          <TreeItem
            itemId="3"
            label={
              <TreeItemLabelWithActionsStory
                labelText='Label 3'
                onUpdate={() => action('Clicked update!')}
              />
            }
          />
        </TreeItem>
      </SimpleTreeView>
    ),
  ],
};
