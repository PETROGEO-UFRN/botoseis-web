import { ErrorLine } from "./styles"

interface ICustomErrorMessageProps {
  content: Array<string> | string
}

export default function CustomErrorMessage({ content }: ICustomErrorMessageProps) {
  return Array.isArray(content) ? (
    <>
      {content.map((message) => (
        <ErrorLine>
          {message}
        </ErrorLine>
      ))}
    </>
  ) : (
    <ErrorLine>
      {content}
    </ErrorLine>
  )
}
