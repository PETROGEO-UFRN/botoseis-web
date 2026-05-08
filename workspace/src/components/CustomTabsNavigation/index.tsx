import type { ReactNode } from 'react'

import Tabs from '@mui/material/Tabs'

import { StaticTabKey } from 'constants/clientPrograms'

import CustomTab from './CustomTab'
import CustomDNDContext from './DefaultDNDList'

import {
  Container,
  TabContent,
} from './styles'

type selectedTabIdType = number | StaticTabKey | undefined

// *** once <T> accepts any type extending "IgenericTab"
// *** it shall be capable to render any matching array
// *** not needing to convert it removing other filds missing at "IgenericTab"
interface ICustomTabsNavigationProps<T extends IgenericTab> {
  tabs: Array<T>
  setTabs: genericSetterType<T>
  selectedTabId: selectedTabIdType
  setSelectedTabId: genericSetterType<selectedTabIdType>
  onRemove?: onRemoveActionType

  children?: ReactNode
  color?: navigationColorType
  orientation?: navigationOrientationType
  tabStaticContent?: ReactNode
}

export default function CustomTabsNavigation<T extends IgenericTab>({
  tabs,
  setTabs,
  selectedTabId,
  setSelectedTabId,
  onRemove,

  children,
  color = "primary",
  orientation = "horizontal",
  tabStaticContent,
}: ICustomTabsNavigationProps<T>) {
  // ? conditional rendering could be a high order component ?
  const removeElementFromState = (tabId: number | StaticTabKey) => {
    if (!tabId || tabId == StaticTabKey.Input || tabId == StaticTabKey.Output)
      return

    const newTabs = tabs.filter((element) => element.id != tabId)

    if (onRemove)
      onRemove(tabId)

    setTabs(newTabs)
    if (selectedTabId == tabId)
      setSelectedTabId(StaticTabKey.Input)
  }

  return Boolean(tabs.length) ? (
    <Container id="containerSample" $orientation={orientation}>
      <CustomDNDContext
        orientation={orientation}
        items={tabs}
        setItems={setTabs}
      >
        <Tabs
          value={selectedTabId}
          onChange={(_, newId) => setSelectedTabId(newId)}
          variant="scrollable"
          scrollButtons="auto"
          orientation={orientation}
        >
          {tabs.map((tab) => (
            <CustomTab
              key={tab.id}
              value={tab.id}
              label={tab.name}
              onRemove={() => removeElementFromState(tab.id)}
              $color={color}
              $orientation={orientation}
              // *** undefined "is_active" is considered as active
              $isActive={tab.is_active ?? true}
            />
          ))}
          {tabStaticContent && tabStaticContent}
        </Tabs>
      </CustomDNDContext>

      {tabs.map(
        (tab) => selectedTabId == tab.id && (
          <TabContent
            key={tab.id}
            $color={color}
            $orientation={orientation}
          >
            {children}
          </TabContent>
        )
      )}
    </Container>
  ) : (
    <></>
  )
}
