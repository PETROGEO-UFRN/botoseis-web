import { PositiveInteger } from 'newtype-ts/lib/PositiveInteger'
import { Positive as PositiveFloat } from 'newtype-ts/lib/Positive'

// !booleans in seismicunix probably be literaly the numbers 0 ou 1
declare type suFileHeader = | "tracl" | "tracr" | "fldr" | "tracf" | "ep" | "cdp" | "cdpt" | "trid" | "nvs" | "nhs" | "duse" | "offset" | "gelev" | "selev" | "sdepth" | "gdel" | "sdel" | "swdep" | "gwdep" | "scalel" | "scalco" | "sx" | "sy" | "gx" | "gy" | "counit" | "wevel" | "swevel" | "sut" | "gut" | "sstat" | "gstat" | "tstat" | "laga" | "lagb" | "delrt" | "muts" | "mute" | "ns" | "dt" | "gain" | "igc" | "igi" | "corr" | "sfs" | "sfe" | "slen" | "styp" | "stas" | "stae" | "tatyp" | "afilf" | "afils" | "nofilf" | "nofils" | "lcf" | "hcf" | "lcs" | "hcs" | "year" | "day" | "hour" | "minute" | "sec" | "timbas" | "trwf" | "grnors" | "grnofr" | "grnlof" | "gaps" | "otrav" | "d1" | "f1" | "d2" | "f2" | "ungpow" | "unscale"

declare type sufilterParametersType = {
  f: string,
  amps: string,
  dt: string,
}

declare type sufilterCommandType = {
  name: "sufilter"
  parameters: sufilterParametersType
}

// 

declare type suwindParametersType = {
  // * propably required, but not required on CLI
  key: string,
  min: string,
  max: string,

  // * not required at all
  verbose: string,
  abs: string,
  j: string,
  skip: string,
  count: string,
  // ?"reject" and "accept" are bad typed?
  reject: string,
  accept: string,
  // ? *** //
  ordered: string,
  dt: string,
  f1: string,
  tmin: string,
  tmax: string,
  itmin: string,
  itmax: string,
  nt: string,
}

declare type suwindCommandType = {
  name: "suwind"
  parameters: suwindParametersType
}

// 

declare type sustackParametersType = {
  key: string,
  normpow: string,
  repeat: string,
  nrepeat: string,
  verbose: string,
}

declare type sustackCommandType = {
  name: "sustack"
  parameters: sustackParametersType
}

// 

declare type sugainParametersType = {
  panel: string,
  tpow: string,
  epow: string,
  etpow: string,
  gpow: string,
  agc: string,
  gagc: string,
  wagc: string,
  trap: string,
  clip: string,
  pclip: string,
  nclip: string,
  qclip: string,
  qbal: string,
  pbal: string,
  mbal: string,
  maxbal: string,
  scale: string,
  norm: string,
  bias: string,
  jon: string,
  verbose: string,
  mark: string
  vred: string
}

declare type sugainCommandType = {
  name: "sugain"
  parameters: sugainParametersType
}

// 

declare type suParametersType = sufilterParametersType | suwindParametersType | sustackParametersType | sugainParametersType

declare type suCommandsQueue = Array<
  sufilterCommandType |
  suwindCommandType |
  sustackCommandType |
  sugainCommandType
>
