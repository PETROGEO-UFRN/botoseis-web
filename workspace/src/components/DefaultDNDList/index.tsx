import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  horizontalListSortingStrategy,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import {
  restrictToVerticalAxis,
  restrictToHorizontalAxis,
  restrictToWindowEdges,
} from '@dnd-kit/modifiers';

import {
  dragActivationDelay,
  dragActivationMouseMovementTolerance
} from 'constants/dnd'

import { IDefaultDNDListProps } from './types'

function getOrientation(orientation: navigationOrientationType) {
  if (orientation == "horizontal")
    return horizontalListSortingStrategy
  return verticalListSortingStrategy
}

function getModifiers(orientation: navigationOrientationType) {
  const modifiers = [restrictToWindowEdges]
  if (orientation == "horizontal")
    return [...modifiers, restrictToHorizontalAxis]
  return [...modifiers, restrictToVerticalAxis]
}

export default function DefaultDNDList<T extends IgenericTab>({
  children,
  orientation = "horizontal",
  items,
  setItems,
}: IDefaultDNDListProps<T>) {
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        delay: dragActivationDelay,
        tolerance: dragActivationMouseMovementTolerance,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  function handleDragEnd(event: any) {
    const { active, over } = event;

    if ((typeof active.id == 'string' || typeof over.id == 'string')) return
    if (active.id == over.id) return

    const oldIndex = items.findIndex((item) => item.id == active.id);
    const newIndex = items.findIndex((item) => item.id == over.id);

    const result = arrayMove(items, oldIndex, newIndex);

    setItems(result);
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
      modifiers={getModifiers(orientation)}
    >
      <SortableContext
        items={items}
        strategy={getOrientation(orientation)}
      >
        {children}
      </SortableContext>
    </DndContext>
  )
}
