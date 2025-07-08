import type { StaticTabKey } from 'constants/StaticTabKey'
declare global {
  type navigationOrientationType = 'horizontal' | 'vertical'
  type navigationColorType = "primary" | "secondary" | "white"

  type onRemoveActionType = (itemId: number | StaticTabKey) => void

  interface IContainerProps {
    $orientation: navigationOrientationType
  }

  interface ICustomTabContainerProps extends IContainerProps {
    $color: navigationColorType
    $isActive: boolean
  }


  interface ICustomTabProps extends ICustomTabContainerProps {
    label: string
    value: number | StaticTabKey
    onRemove(): void
  }

  interface ITabContentProps extends IContainerProps {
    $color: navigationColorType
  }
}
