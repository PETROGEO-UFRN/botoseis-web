import { create } from 'zustand';
import type { VariantType } from 'notistack';


type notificationMessageType = {
  content: string | Error
  variant?: VariantType
}

interface INotificationStore {
  notificationMessage: notificationMessageType | null
  triggerNotification: (value: notificationMessageType) => void
}

const useNotificationStore = create<INotificationStore>((set) => ({
  notificationMessage: null,
  triggerNotification: ({ content, variant }) => {
    set({ notificationMessage: { content, variant } })
  },
}));

export default useNotificationStore;
