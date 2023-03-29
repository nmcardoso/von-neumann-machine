import { createContext, Dispatch, ReactElement, useContext, useReducer } from 'react'
import localforage from 'localforage'

const initialState = {
  schemaVersion: 1,
  memory: [],
  registers: {
    accumulator: null,
    pc: null,
  },
}

const persistStateAsync = (state) => {
  const s = { ...state }
  localforage.setItem('machineState', s, (err, value) => {
    if (err) console.error(err)
  })
}

const loadSavedStateAction = (state, action) => {
  return action.payload
}

const reducer = (state, action) => {
  switch (action.type) {
    case 'loadSavedState':
      return loadSavedStateAction(state, action)
    default:
      console.error(`Action ${action.type} not found`)
      return { ...state }
  }
}


export const MachineContext = createContext({
  mcState: initialState,
  mcDispatch: () => { }
})


export const MachineProvider = ({ children }) => {
  const [mcState, mcDispatch] = useReducer(reducer, initialState)
  return (
    <MachineContext.Provider value={{ mcState, mcDispatch }}>
      {children}
    </MachineContext.Provider>
  )
}


export const useMachine = () => useContext(MachineContext)