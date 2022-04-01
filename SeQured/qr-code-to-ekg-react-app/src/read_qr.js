//qr code reader
//source: https://medium.com/@johndoan42/how-to-implement-a-qr-code-reader-into-your-react-application-3638e466dc79

import QrReader from 'react-qr-scanner'
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'
import {Plot, LineSeries, Heading} from 'react-plot'



//js


const QrContainer = () =>
{

    const [scanValue, setScanValue] = React.useState(null);

    const previewStyle ={
        height:700,
        width:1000,
        display: 'flex',
        justifyContent: "center"
    }

    const camStyle = {
        display: 'flex',
        justifyContent: "center",
        marginTop: '-50px'
    }

    const textStyle = {
        fontSize: '30px',
        textAlign: 'center',
        marginTop: '-50px'
    }

    // Parse data from this.state.result

    // Decode the String
    var decodedString =  null;
    var mint_array = []
    if(scanValue)
    {
        decodedString = window.atob(scanValue.text);
        for (var i = 0; i < decodedString.length-1; i=i+2) {
            var letter1 = decodedString.charCodeAt(i);
            var letter2 = decodedString.charCodeAt(i + 1);
            var int = 0;
            if (letter2 > 127) {
                int = (letter2 * 256) + letter1 - 65536;
            } else {
                int = (letter2 * 256) + letter1;
            }
            mint_array.push(int);
        }
        console.log(mint_array)
    }

    return(
        <React.Fragment>
            { !scanValue ?
                <div style={camStyle}>
                    <QrReader
                        facingMode={"rear"}
                        delay={300}
                        style={previewStyle}
                        onError={e => console.log(e)}
                        onScan={setScanValue}
                    />
                </div>
                    :
                <div>
                <Plot
                    width={700}
                    height={500}
                    margin={{ bottom: 50, left: 90, top: 50, right: 100 }}
                >
                    <Heading
                        title="Electrical characterization"
                        subtitle="current vs voltage"
                    />
                    <LineSeries
                        data={
                            mint_array.map((v,i) => ({
                                x: i , y:v
                            }))
                        }
                        xAxis="x"
                        yAxis="y"
                        lineStyle={{ strokeWidth: 3 }}
                        label="Vg = 7V"
                        displayMarker={false}
                    />
                </Plot>
            </div>
            }
        </React.Fragment>
    )

}

export default QrContainer
