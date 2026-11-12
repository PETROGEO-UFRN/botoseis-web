declare type environmentType = 'development' | 'production' | 'test'

declare interface IAppFactoryProps {
  environment?: environmentType
}

declare interface IRouteFactoryProps extends IAppFactoryProps {}

declare interface IMiddlewareFactoryProps extends IAppFactoryProps {}
