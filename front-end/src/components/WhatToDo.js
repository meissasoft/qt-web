import React from 'react'
import Live from "../assets/icons/live.png"
import Data from "../assets/icons/data.png"

function WhatToDo({goToPage}) {
  return (
    <div className='maindiv'>
      <div style={{display:"flex" , justifyContent:"center" , alignItems:"center" ,flexDirection :"column" , height:"100%"}}>
        <h1 className='text'>
        What would you like to do?
        </h1>
        <div style={{width:"60%" , display :"flex" ,justifyContent:"space-around" , marginTop:"40px"}}>
            <button className='btn' onClick={()=>goToPage(4)}>
              <img src={Live} alt="" /><br />
                Start Live Data
            </button>
            <button className='btn' onClick={()=>goToPage(4)}>
              <img src={Data} alt="" width={30}/><br />
                Show Old Data
            </button>
        </div>
      </div>
    </div>
  )
}

export default WhatToDo;
