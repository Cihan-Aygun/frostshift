import unittest
from frostshift.engine import run,compare
class Tests(unittest.TestCase):
 def test_conservation_and_capacity(self):
  for seed in range(10):
   for policy in ('none','depot','transfer'):
    s=run(seed=seed,policy=policy)
    self.assertEqual(s['initial']+s['delivered'],s['sold']+s['remaining'])
    for day in s['history']:
     for stock in day['stock']:self.assertTrue(all(v>=0 for v in stock));self.assertLessEqual(sum(stock),240)
    for day in range(1,8):
     if policy=='transfer':self.assertLessEqual(sum(e['quantity'] for e in s['events'] if e['day']==day),50)
 def test_common_demand(self):
  s=compare()['scenarios'];self.assertEqual(len({x['sold']+x['lost'] for x in s}),1)
 def test_reproducible(self):self.assertEqual(run(),run())
 def test_economic_gate(self):
  for e in run()['events']:self.assertGreater(e['quantity']*18,e['cost'])
 def test_invalid(self):
  with self.assertRaises(ValueError):run(heat=-1)
if __name__=='__main__':unittest.main()
