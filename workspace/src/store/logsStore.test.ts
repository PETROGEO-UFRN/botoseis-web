import { cleanup } from '@testing-library/react'

import { renderHook } from '@testing-library/react-hooks'
import { useLogsStore } from "./logsStore"

describe("Logs Store", () => {
  const getMockLog = (fakeId: number = 0): IprocessLogs => ({
    executionSimplifiedString: "sufilter < input.su > output.su",
    logMessage: `log message ${fakeId}`,
    returncode: 1,
    processStartTime: "2020-01-01 04:03:18.729296",
    executionEndTime: "2020-01-01 04:04:18.729296",
  })

  afterEach(cleanup)
  it("Should be empty Map", () => {
    const { result } = renderHook(() => useLogsStore())

    expect(result.current.logs).toBeInstanceOf(Map)
    expect(result.current.logs).toEqual(new Map())
    expect(result.current.logs.size).toBe(0)
  })

  it("Should push new error log", () => {
    const { result } = renderHook(() => useLogsStore())
    result.current.pushNewLog(0, getMockLog())

    expect(result.current.logs).toBeInstanceOf(Map)
    expect(result.current.logs.get(0)).toEqual([getMockLog()])
  })

  it("Should push new error log at non initialized position", () => {
    const { result } = renderHook(() => useLogsStore())
    result.current.pushNewLog(37, getMockLog())

    expect(result.current.logs).toBeInstanceOf(Map)
    const logs: Array<IprocessLogs> | undefined = result.current.logs.get(37)
    expect(logs).toBeDefined()
    if (logs) {
      expect(logs[0].executionSimplifiedString).toEqual(getMockLog().executionSimplifiedString)
      expect(logs[0].logMessage).toEqual(getMockLog().logMessage)
      expect(logs[0].returncode).toEqual(getMockLog().returncode)
      expect(logs[0].processStartTime).toEqual(getMockLog().processStartTime)
      expect(logs[0].executionEndTime).toEqual(getMockLog().executionEndTime)
    }
  })

  it("Should push new success log", () => {
    const { result } = renderHook(() => useLogsStore())
    const successLog = getMockLog(0)
    successLog.returncode = 0
    result.current.pushNewLog(99, successLog)

    expect(result.current.logs).toBeInstanceOf(Map)
    const logs: Array<IprocessLogs> | undefined = result.current.logs.get(99)
    expect(logs).toBeDefined()
    if (logs) {
      expect(logs[0].executionSimplifiedString).toEqual(getMockLog().executionSimplifiedString)
      expect(logs[0].logMessage).toEqual("Success")
      expect(logs[0].returncode).toEqual(0)
      expect(logs[0].processStartTime).toEqual(getMockLog().processStartTime)
      expect(logs[0].executionEndTime).toEqual(getMockLog().executionEndTime)
    }
  })

  it("Should push multiple new error logs", () => {
    const { result } = renderHook(() => useLogsStore())
    result.current.pushNewLog(3, getMockLog(1))
    result.current.pushNewLog(3, getMockLog(2))
    result.current.pushNewLog(3, getMockLog(3))
    result.current.pushNewLog(3, getMockLog(4))

    expect(result.current.logs).toBeInstanceOf(Map)
    expect(result.current.logs.get(3)).toEqual([
      getMockLog(1),
      getMockLog(2),
      getMockLog(3),
      getMockLog(4),
    ])
  })

  it("Should push new error logs to multiple keys", () => {
    const { result } = renderHook(() => useLogsStore())
    result.current.pushNewLog(7, getMockLog(1))
    result.current.pushNewLog(7, getMockLog(2))

    result.current.pushNewLog(9, getMockLog(1))
    result.current.pushNewLog(9, getMockLog(2))

    result.current.pushNewLog(2, getMockLog(1))
    result.current.pushNewLog(2, getMockLog(2))

    expect(result.current.logs).toBeInstanceOf(Map)
    expect(result.current.logs.get(7)).toEqual([
      getMockLog(1),
      getMockLog(2),
    ])
    expect(result.current.logs.get(9)).toEqual([
      getMockLog(1),
      getMockLog(2),
    ])
    expect(result.current.logs.get(2)).toEqual([
      getMockLog(1),
      getMockLog(2),
    ])
  })
})
