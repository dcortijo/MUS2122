using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using FMODUnity;

public class PlayerController : MonoBehaviour
{
    [SerializeField] StudioEventEmitter emitterEngine;

    private void Start()
    {
        emitterEngine.Play();
        //emitterEngine.SetParameter("Efficiency", Mathf.Clamp(GetComponent<Generator>().hp / GetComponent<Generator>().maxHp, 0, 0.99f));
    }

    private void Update()
    {
        if (emitterEngine.IsPlaying())
        {
            //emitterEngine.SetParameter("Efficiency", Mathf.Clamp(GetComponent<Generator>().hp / GetComponent<Generator>().maxHp, 0, 0.99f));
        }
    }
}
