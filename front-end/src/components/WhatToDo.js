import React from 'react'

function WhatToDo({goToPage}) {
  return (
    <div className='maindiv'>
      <div style={{display:"flex" , justifyContent:"center" , alignItems:"center" ,flexDirection :"column" , height:"100%"}}>
        <h1 className='text'>
        What would you like to do?
        </h1>
        <div style={{width:"50%" , display :"flex" ,justifyContent:"space-around" , marginTop:"40px"}}>
            <button className='btn' onClick={()=>goToPage(4)}>
                Start Live Data
            </button>
            <button className='btn' onClick={()=>goToPage(4)}>
                Show Old Data
            </button>
        </div>
      </div>
    </div>
  )
}

export default WhatToDo;
