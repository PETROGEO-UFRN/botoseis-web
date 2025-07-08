import { renderHook } from '@testing-library/react-hooks'
import useNotificationStore from "./notificationStore"

describe("Notification Store", () => {
  it("Should be null", () => {
    const { result } = renderHook(() => useNotificationStore())
    expect(result.current.notificationMessage).toBe(null)
  })

  it("Should create notification", () => {
    const { result } = renderHook(() => useNotificationStore())
    result.current.triggerNotification({
      content: "Hello!",
    })
    expect(result.current.notificationMessage).toEqual({
      content: "Hello!",
      variant: undefined,
    })
  })

  it("Should create notification", () => {
    const { result } = renderHook(() => useNotificationStore())
    result.current.triggerNotification({
      content: "Hello!",
    })
    expect(result.current.notificationMessage).toEqual({
      content: "Hello!",
      variant: undefined,
    })
  })

  it("Should create error notification", () => {
    const { result } = renderHook(() => useNotificationStore())
    const sampleError = new Error("Sample error message")
    result.current.triggerNotification({
      content: sampleError,
      variant: 'error',
    })
    expect(result.current.notificationMessage).toEqual({
      content: sampleError,
      variant: 'error',
    })
  })

  it("Should not require variant to create error notification", () => {
    const { result } = renderHook(() => useNotificationStore())
    const sampleError = new Error("Sample error message without variant")
    result.current.triggerNotification({
      content: sampleError,
    })
    expect(result.current.notificationMessage).toEqual({
      content: sampleError,
      variant: undefined,
    })
  })
})
