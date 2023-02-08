import React from 'react'

function SaveInfo({goToPage}) {
  return (
    
    <div className='maindiv' style={{display:"flex" , flexDirection :"column" , alignItems:"center ", justifyContent :"center"}}>
      <p style={{ fontSize:"30px" , fontWeight:"500" , marginBottom:"2rem"}}>
      What would you like to name the new file?
      </p>
      <input className='form-control' ></input>
      <button className='btn' style={{marginTop:"2rem"}} onClick={()=>goToPage(9)}>
    Go
      </button>
    </div>
  )
}

export default SaveInfo
