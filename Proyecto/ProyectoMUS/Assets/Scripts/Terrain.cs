using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using FMODUnity;

public class Terrain : MonoBehaviour
{
    [SerializeField] StudioEventEmitter addEmitter;    // Emisor de la melod�a adicional, siempre activo pero con volumen modulado cuando no le conviene
    public float secondsToFade = 3;

    private float currentVolume = 0;

    // Start is called before the first frame update
    void Start()
    {
        addEmitter.Play();
        addEmitter.SetParameter("Volumen", currentVolume);
    }

    // Update is called once per frame
    void Update()
    {
        currentVolume -= (1 / secondsToFade) * Time.deltaTime;
        currentVolume = Mathf.Max(currentVolume, 0);
        //Debug.Log(currentVolume);
        addEmitter.SetParameter("Volumen", currentVolume);
    }

    private void OnTriggerStay(Collider other)
    {
        PlayerController play = other.GetComponent<PlayerController>();

        if (play)
        {
            currentVolume += ((1/secondsToFade) * Time.deltaTime) * 2; // Este 2 es para contraarestar el fade out del update, que que peerza si no tener que mirar si est� o no en el collider
            currentVolume = Mathf.Min(currentVolume, 1);
        }
    }
}
