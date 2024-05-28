import useData from "../hooks/useAxios"
import React from 'react'

export default function EntrysAll() {
  const {data, error, isLoading} = useData(`${import.meta.env.}`)

  return (
    <div>
      Hola
    </div>
  )
}
